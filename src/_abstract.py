from abc import ABC, abstractmethod
from typing import Optional, TypedDict, List, Dict, Union


class LocalStateOutput(TypedDict):
    asset_balances: Dict[
        int, int
    ]  # { asset_id: asset_balance (no decimals) }, negative balances allowed for ALGO use 0


class GlobalStateOutput(TypedDict):
    asset_balances: Dict[
        int, int
    ]  # { asset_id: asset_balance (no decimals) }, negative balances allowed, for ALGO use 0
    timestamp_from: Optional[int]  # unix timestamp
    timestamp_to: Optional[int]  # unix timestamp
    round_from: Optional[int]
    round_to: Optional[int]


class ApplicationType(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        # Returns name of Application Type (e.g. "Algofi Lending Protocol")
        pass

    @property
    @abstractmethod
    def key(self) -> str:
        # Returns a 4 letter application type identifier (e.g. "AF1L")
        pass

    @abstractmethod
    def fetch_static_application_ids(self) -> List[int]:
        # Returns a list of application ids that are not dynamic and not need to be fetched again
        pass

    @abstractmethod
    def fetch_dynamic_application_ids(self, last_application_id: int) -> List[int]:
        # Return a list of application ids that are dynamic
        # The function should make use of last_application_id to only return applications with higher ids
        pass

    @abstractmethod
    def is_local_state_valid(self, local_state: Dict[str, Union[str, int]]) -> bool:
        # Return True if passed dict is a valid application state for wallet, else False
        # Check if local state contains are required for parsing keys and if those keys seem valid
        # If keys are unused in parsing, do not check for their existence
        pass

    @abstractmethod
    def is_global_state_valid(self, global_state: Dict[str, Union[str, int]]) -> bool:
        # Return True if passed dict is a valid application state, else False
        # Check if global state contains are required for parsing keys and if those keys seem valid
        # If keys are unused in parsing, do not check for their existence
        pass

    @abstractmethod
    def parse_local_state(
        self, local_state: Dict[str, Union[str, int]]
    ) -> LocalStateOutput:
        # Return parsed local state for given wallet
        pass

    @abstractmethod
    def parse_global_state(
        self, global_state: Dict[str, Union[str, int]]
    ) -> GlobalStateOutput:
        # Return parsed global state for given application
        pass
