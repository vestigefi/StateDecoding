# This is a template file for easy start

from typing import Dict, Union, List
from src.common.common import get_application_state, get_wallet_state
from src.common.abstract import (
    ApplicationType,
    UsageType,
    GlobalStateOutput,
    LocalStateOutput,
    ApplicationMeta
)


class Template(ApplicationType):
    @staticmethod
    def get_meta() -> ApplicationMeta:
        # TODO
        return {
            "name": "Template",
            "key": "TMPL",
            "type": UsageType.LENDING
        }

    @staticmethod
    def fetch_static_application_ids(self) -> List[int]:
        application_ids = []
        # TODO
        return application_ids

    @staticmethod
    def fetch_dynamic_application_ids(last_application_id: int) -> List[int]:
        application_ids = []
        # TODO
        return application_ids

    @staticmethod
    def is_wallet_state_valid(wallet_state: Dict[str, Union[str, int]]) -> bool:
        # TODO
        return True

    @staticmethod
    def is_application_state_valid(application_state: Dict[str, Union[str, int]]) -> bool:
        # TODO
        return True

    @staticmethod
    def parse_wallet_state(
        wallet_state: Dict[str, Union[str, int]]
    ) -> LocalStateOutput:
        state_output: LocalStateOutput = {"asset_balances": dict()}
        # TODO
        return state_output

    @staticmethod
    def parse_application_state(
        application_state: Dict[str, Union[str, int]]
    ) -> GlobalStateOutput:
        state_output: GlobalStateOutput = {
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
        wallet_state = get_wallet_state("VESTIG3V77NNVBT5SM636UKAZ3M5OQHM76TC5622RQ4Q2XUCYZ5E4ENB3E", 784136787)
        if Template.is_wallet_state_valid(wallet_state):
            values = Template.parse_wallet_state(wallet_state)
            # TODO
            # check values, return False if any of them are wrong
        application_state = get_application_state(777747637)
        if Template.is_application_state_valid(application_state):
            values = Template.parse_application_state(application_state)
            # TODO
            # check values, return False if any of them are wrong
        return True


if __name__ == '__main__':
    Template.test_application_type()
