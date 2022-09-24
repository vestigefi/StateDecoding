# This is a template file for easy start

from typing import Dict, Union, List
from src.common.abstract import ApplicationType, UsageType, GlobalStateOutput, LocalStateOutput


class Template(ApplicationType):
    @property
    def name(self) -> str:
        # TODO
        return "Template"

    @property
    def key(self) -> str:
        # TODO
        return "0TMP"

    @property
    def type(self) -> str:
        # TODO
        return UsageType.LENDING

    def fetch_static_application_ids(self) -> List[int]:
        application_ids = []
        # TODO
        return application_ids

    def fetch_dynamic_application_ids(self, last_application_id: int) -> List[int]:
        application_ids = []
        # TODO
        return application_ids

    def is_local_state_valid(self, local_state: Dict[str, Union[str, int]]) -> bool:
        # TODO
        return False

    def is_global_state_valid(self, global_state: Dict[str, Union[str, int]]) -> bool:
        # TODO
        return True

    def parse_local_state(self, local_state: Dict[str, Union[str, int]]) -> LocalStateOutput:
        state_output: LocalStateOutput = {
            "asset_balances": dict()
        }
        # TODO
        return state_output

    def parse_global_state(self, global_state: Dict[str, Union[str, int]]) -> GlobalStateOutput:
        state_output: GlobalStateOutput = {
            "asset_balances": dict(),
            "timestamp_from": None,
            "timestamp_to": None,
            "round_from": None,
            "round_to": None
        }
        # TODO
        return state_output
