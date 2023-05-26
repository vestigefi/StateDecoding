# This is a HumbleFarm file for easy start

from typing import Dict, Union, List
from src.common.common import (
    get_application_state,
    get_wallet_state,
    indexer_get_request,
    node_get_request,
)
from src.common.abstract import (
    ApplicationType,
    UsageType,
    ApplicationStateOutput,
    WalletStateOutput,
    ApplicationMeta,
)
import base64


def get_bytes_value(data: bytes, index: int, offset: int):
    if data and isinstance(data, bytes) and len(data) > index * 8 + offset:
        a = data[index * 8 + offset : index * 8 + offset + 8]
        return int.from_bytes(data[index * 8 + offset : index * 8 + offset + 8], "big")


class HumbleFarm(ApplicationType):
    MANAGER_APP_ID = 830314595

    @staticmethod
    def get_meta() -> ApplicationMeta:
        # TODO
        return {"name": "Humble Farm", "key": "HMBLFARM", "type": UsageType.FARMING}

    @staticmethod
    def fetch_static_application_ids() -> List[int]:
        # no static ids, each farm has their own id
        return []

    @staticmethod
    def fetch_dynamic_application_ids(last_application_id: int) -> List[int]:
        application_ids = []
        response = indexer_get_request(
            f"v2/transactions?application-id={HumbleFarm.MANAGER_APP_ID}"
        )
        transactions = response.get("transactions", [])
        for transaction in response.get("transactions", []):
            application_ids = transaction.get("application-transaction", {}).get(
                "foreign-apps"
            )
            application_id = application_ids[0] if len(application_ids) > 0 else None
            if application_id and application_id > last_application_id:
                application_ids.append(application_id)
        print(application_ids)
        return list(set(application_ids))

    @staticmethod
    def is_wallet_state_valid(wallet_state: Dict[str, Union[str, int]]) -> bool:
        # ideally this would be more complex, i.e. checking if the values there make sense
        if "AA==" in wallet_state:
            return True
        return False

    @staticmethod
    def is_application_state_valid(
        application_state: Dict[str, Union[str, int]]
    ) -> bool:
        # ideally this would be more complex, i.e. checking if the values there make sense
        if "AA==" in application_state:
            return True
        return False

    @staticmethod
    def parse_wallet_state(
        wallet_state: Dict[str, Union[str, int]],
        application_data: ApplicationStateOutput,
    ) -> WalletStateOutput:
        state_output: WalletStateOutput = {"asset_balances": dict()}
        asset_ids = application_data.get("asset_balances").keys()
        # ordering in application data asset balances is kept - always return lp token on first position
        lp_token_id = asset_ids[0] if len(asset_ids) > 0 else None
        if lp_token_id:
            state_output["asset_balances"][lp_token_id] = get_bytes_value(
                base64.b64decode(wallet_state["AA=="]), 2, 1
            )
        return state_output

    @staticmethod
    def parse_application_state(
        application_state: Dict[str, Union[str, int]]
    ) -> ApplicationStateOutput:
        state_output: ApplicationStateOutput = {
            "asset_balances": dict(),
            "timestamp_from": None,
            "timestamp_to": None,
            "round_from": None,
            "round_to": None,
        }
        lp_token_id = get_bytes_value(base64.b64decode(application_state["AA=="]), 5, 0)
        # maybe get the amount while you're at it
        state_output["asset_balances"][lp_token_id] = 0
        return state_output

    @staticmethod
    def test_application_type() -> bool:
        # TODO idk fix this shit
        # use addresses and application ids that will not break over time
        test_application_ids = HumbleFarm.fetch_dynamic_application_ids(0)
        print(test_application_ids)
        test_wallet_address = (
            "MEME5QEUYPK6T3DVHAU6A45RYC4JHMU3U45OCCCWZJH47HVKGKW3PZP5AM"
        )
        response = node_get_request(f"v2/accounts/{test_wallet_address}")
        wallet_apps = response.get("apps-local-state")
        application_ids = [app.get("id") for app in wallet_apps]
        print(application_ids)
        for application_id in application_ids:
            app_state = get_application_state(application_id)
            print(app_state)
            print(
                HumbleFarm.parse_application_state(
                    get_application_state(application_id)
                )
            )
            if application_id in test_application_ids:
                wallet_state = get_wallet_state(test_wallet_address, application_id)
                if HumbleFarm.is_wallet_state_valid(wallet_state):
                    values = HumbleFarm.parse_wallet_state(wallet_state)
                    print(values)
                    # TODO
                    # check values, return False if any of them are wrong

        return True


if __name__ == "__main__":
    HumbleFarm.test_application_type()
