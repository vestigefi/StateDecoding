from abc import ABC, abstractmethod
from typing import Optional, TypedDict, List, Dict, Union


class UsageType:
    # one-sided staking for coins, e.g. VEST -> VEST
    STAKING = "STKE"
    # one-sided and two-sided staking for coins, e.g. VEST/ALGO LP -> VEST
    FARMING = "FARM"
    # lending/borrowing protocols
    LENDING = "LEND"


class RawWalletState(TypedDict):
    # TODO: Type this properly.
    assets: Dict
    local_state: Dict
    created_apps: Dict


class WalletStateOutput(TypedDict):
    asset_balances: Dict[
        int, int
    ]  # { asset_id: asset_balance (no decimals) }, negative balances allowed for ALGO use 0


class ApplicationStateOutput(TypedDict):
    asset_balances: Dict[
        int, int
    ]  # { asset_id: asset_balance (no decimals) }, negative balances allowed, for ALGO use 0
    timestamp_from: Optional[int]  # unix timestamp
    timestamp_to: Optional[int]  # unix timestamp
    round_from: Optional[int]
    round_to: Optional[int]
    application_id: int


class ApplicationMeta(TypedDict):
    name: str
    key: str
    type: UsageType


class ApplicationType(ABC):
    @staticmethod
    @abstractmethod
    def get_meta() -> ApplicationMeta:
        # Returns application metadata used internally
        pass

    @staticmethod
    @abstractmethod
    def fetch_static_application_ids() -> List[int]:
        # Returns a list of application ids that are not dynamic and not need to be fetched again
        pass

    @staticmethod
    @abstractmethod
    def fetch_dynamic_application_ids(last_application_id: int) -> List[int]:
        # Return a list of application ids that are dynamic
        # The function should make use of last_application_id to only return applications with higher ids
        pass

    @staticmethod
    @abstractmethod
    def fetch_local_application_ids(raw_wallet_state) -> List[int]:
        # Return a list of application ids that are local to the wallet, i.e. created apps.
        pass

    @staticmethod
    @abstractmethod
    def is_wallet_state_valid(
        wallet_state: Dict[str, Union[str, int]],
        application_date: ApplicationStateOutput,
    ) -> bool:
        # Return True if passed dict is a valid application state for wallet, else False
        # Check if state contains required for parsing keys and if those keys seem valid
        # If keys are unused in parsing, do not check for their existence
        pass

    @staticmethod
    @abstractmethod
    def is_application_state_valid(
        application_state: Dict[str, Union[str, int]]
    ) -> bool:
        # Return True if passed dict is a valid application state, else False
        # Check if state contains required for parsing keys and if those keys seem valid
        # If keys are unused in parsing, do not check for their existence
        pass

    @staticmethod
    @abstractmethod
    def parse_wallet_state(
        wallet_state: Dict[str, Union[str, int]],
        application_data: ApplicationStateOutput,
    ) -> WalletStateOutput:
        # Return parsed local state for given wallet
        pass

    @staticmethod
    @abstractmethod
    def parse_application_state(
        application_state: Dict[str, Union[str, int]]
    ) -> ApplicationStateOutput:
        # Return parsed global state for given application
        pass

    @staticmethod
    @abstractmethod
    def test_application_type() -> bool:
        # Dummy function that should call any of the known IDs of this application type using above functions
        # and check if data is valid
        # use get_application_state() from _common
        # Return True if valid, else False
        pass
