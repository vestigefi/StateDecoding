# This is a HumbleFarm file for easy start

from typing import Dict, Union, List
from src.common.common import (
    get_application_state,
    get_wallet_state,
    indexer_get_request,
    node_get_request,
    test_application_type,
)
from src.common.abstract import (
    ApplicationType,
    UsageType,
    ApplicationStateOutput,
    WalletStateOutput,
    ApplicationMeta,
    RawWalletState,
)
import base64


def get_bytes_value(data: bytes, index: int, offset: int):
    if data and isinstance(data, bytes) and len(data) > index * 8 + offset:
        a = data[index * 8 + offset : index * 8 + offset + 8]
        return int.from_bytes(data[index * 8 + offset : index * 8 + offset + 8], "big")


class HumbleFarm(ApplicationType):
    MANAGER_APP_IDS = [830314595, 857348615]

    @staticmethod
    def get_meta() -> ApplicationMeta:
        # TODO
        return {"name": "Humble Farm", "key": "HMBLFARM", "type": UsageType.FARMING}

    @staticmethod
    def fetch_static_application_ids() -> List[int]:
        # no static ids, each farm has their own id
        return []

    @staticmethod
    def fetch_local_application_ids(raw_wallet_state) -> List[int]:
        # no local application ids, the user does not create their own escrow app.
        return []

    @staticmethod
    def fetch_dynamic_application_ids(last_application_id: int) -> List[int]:
        application_ids = []
        for manager_app_id in HumbleFarm.MANAGER_APP_IDS:
            response = indexer_get_request(
                f"v2/transactions?application-id={manager_app_id}"
            )
            transactions = response.get("transactions", [])
            for transaction in transactions:
                tx_application_ids = transaction.get("application-transaction", {}).get(
                    "foreign-apps"
                )
                application_id = (
                    tx_application_ids[0] if len(tx_application_ids) > 0 else None
                )
                if application_id and application_id > last_application_id:
                    application_ids.append(application_id)
        return list(set(application_ids))

    @staticmethod
    def is_application_state_valid(
        application_state: Dict[str, Union[str, int]]
    ) -> bool:
        # ideally this would be more complex, i.e. checking if the values there make sense
        if "AA==" in application_state:
            return True
        return False

    @staticmethod
    def is_wallet_state_valid(
        wallet_state: RawWalletState, application_id: int
    ) -> bool:
        # ideally this would be more complex, i.e. checking if the values there make sense
        if "AA==" in wallet_state["local_state"].get(application_id):
            return True
        return False

    @staticmethod
    def parse_wallet_state(
        wallet_state: RawWalletState,
        application_data: ApplicationStateOutput,
        application_id: int,
    ) -> WalletStateOutput:
        state_output: WalletStateOutput = {"asset_balances": dict()}
        asset_ids = list(application_data.get("asset_balances", {}).keys())

        # ordering in application data asset balances is kept - always return lp token on first position
        lp_token_id = asset_ids[0] if len(asset_ids) > 0 else None

        if lp_token_id:
            state_output["asset_balances"][lp_token_id] = get_bytes_value(
                # This state always exists if is_wallet_state_valid is OK.
                base64.b64decode(wallet_state["local_state"][application_id]["AA=="]),
                2,
                1,
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
        test_wallets = {
            "JTJ5JVY75TH2SILVAJU4SQRRY2XWEIT6VKTEQMII3QTXZVNT3RWUGUKFSA": {
                "asset_balances": {1049108376: 38699447, 1055369800: 716722137}
            }
        }

        for wallet, expected_result in test_wallets.items():
            res = test_application_type(wallet, HumbleFarm)
            print(res, expected_result)
            if res != expected_result:
                return False

        return True


if __name__ == "__main__":
    HumbleFarm.test_application_type()
