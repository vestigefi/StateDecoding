# This is a template file for easy start

from typing import Dict, Union, List
from src.common.common import (
    get_application_state,
    get_wallet_state,
    test_application_type,
)
from src.common.abstract import (
    ApplicationType,
    UsageType,
    ApplicationStateOutput,
    WalletStateOutput,
    ApplicationMeta,
)


class Template(ApplicationType):
    @staticmethod
    def get_meta() -> ApplicationMeta:
        # TODO
        return {"name": "Template", "key": "TMPL", "type": UsageType.LENDING}

    @staticmethod
    def fetch_static_application_ids() -> List[int]:
        application_ids = []
        # TODO
        return application_ids

    @staticmethod
    def fetch_dynamic_application_ids(last_application_id: int) -> List[int]:
        application_ids = []
        # TODO
        return application_ids

    @staticmethod
    def fetch_local_application_ids(raw_wallet_state) -> List[int]:
        application_ids = []
        # TODO
        return application_ids

    @staticmethod
    def is_wallet_state_valid(
        wallet_state: Dict[str, Union[str, int]],
        application_data: ApplicationStateOutput,
    ) -> bool:
        # TODO
        return True

    @staticmethod
    def is_application_state_valid(
        application_state: Dict[str, Union[str, int]]
    ) -> bool:
        # TODO
        return True

    @staticmethod
    def parse_wallet_state(
        wallet_state: Dict[str, Union[str, int]],
        application_data: ApplicationStateOutput,
    ) -> WalletStateOutput:
        state_output: WalletStateOutput = {"asset_balances": dict()}
        # TODO
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
        # TODO
        return state_output

    @staticmethod
    def test_application_type() -> bool:
        # use addresses and application ids that will not break over time
        test_wallet_address = (
            "VESTIG3V77NNVBT5SM636UKAZ3M5OQHM76TC5622RQ4Q2XUCYZ5E4ENB3E"
        )
        test_application_id = 784136787
        application_state = get_application_state(test_application_id)
        if Template.is_application_state_valid(application_state):
            application_data = Template.parse_application_state(application_state)
            # TODO
            # check values, return False if any of them are wrong
            wallet_state = get_wallet_state(test_wallet_address, test_application_id)
            if Template.is_wallet_state_valid(wallet_state, application_data):
                values = Template.parse_wallet_state(wallet_state, application_data)
                # TODO
                # check values, return False if any of them are wrong
                return True
        return False

    @staticmethod
    def test_application_type() -> bool:
        test_wallets = {
            "JTJ5JVY75TH2SILVAJU4SQRRY2XWEIT6VKTEQMII3QTXZVNT3RWUGUKFSA": {
                "asset_balances": {}
            }
        }

        for wallet, expected_result in test_wallets.items():
            res = test_application_type(wallet, Template)
            print(res, expected_result)
            if res != expected_result:
                return False

        return True


if __name__ == "__main__":
    Template.test_application_type()
