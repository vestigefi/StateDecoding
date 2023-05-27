# This is a HumbleFarm file for easy start
from algosdk.logic import get_application_address
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


class PactFarm(ApplicationType):
    ESCROW_BYTECODE = [
        'CCAEAAEEBiYDC01hc3RlckFwcElEAQEBADIJMQASRDEZQADyMRhAAEU2GgCABDiIGnESRCg2GgEXwDJnsSWyEDYaAhfAMrIYgAS3NV/RshoisgGzsSSyEDIKshQishI2GgMXwDCyESKyAbNCANU2GgCABHiCLPASQABONhoAgAS3WNjREkAAKTYaAIAEm+QoGxJAAAEAsSOyEDYaARfAHLIHIrIBNhoCVwIAsgWzQgCSsSOyEDIJsgcyCmAyCngJsggisgGzQgB6sSSyEDIJshQ2GgIXshI2GgEXwDCyESKyAbOxJbIQKGSyGIAEwxQK57IaKbIaKrIaKbIaKrIaMgmyHDIIsjI2GgEXwDCyMCKyAbNCAC0xGYEFEkAAAQAyCShkYRREsSSyEDYwALIRMgmyFSKyAbOxI7IQMgmyCSKyAbMjQw==',
    ]

    @staticmethod
    def get_meta() -> ApplicationMeta:
        # TODO
        return {"name": "Pact Farm", "key": "PACTFARM", "type": UsageType.FARMING}

    @staticmethod
    def fetch_static_application_ids() -> List[int]:
        # no static ids, each farm has their own id
        return []

    @staticmethod
    def fetch_dynamic_application_ids(last_application_id: int) -> List[int]:
        return []
    
    @staticmethod
    def fetch_local_application_ids(raw_wallet_state: RawWalletState) -> List[int]:
        return list(raw_wallet_state["created_apps"].keys())

    @staticmethod
    def is_application_state_valid(
        application_state: Dict[str, Union[str, int]]
    ) -> bool:
        # There is no application state, we always approve
        return True

    @staticmethod
    def is_wallet_state_valid(
        wallet_state: RawWalletState, application_id: int
    ) -> bool:
        # ideally this would be more complex, i.e. checking if the values there make sense
        bytecode = wallet_state["created_apps"].get(application_id, "")
        if bytecode in PactFarm.ESCROW_BYTECODE:
            return True
        return False

    @staticmethod
    def parse_wallet_state(
        wallet_state: RawWalletState,
        application_data: ApplicationStateOutput,
        application_id: int,
    ) -> WalletStateOutput:
        state_output: WalletStateOutput = {"asset_balances": dict()}

        # ordering in application data asset balances is kept - always return lp token on first position

        res = node_get_request((f"v2/accounts/{get_application_address(application_id)}"))
        for asset in res.get("assets"):
            id = asset.get("asset-id")
            amount = asset.get("amount")
            state_output["asset_balances"].update({id: amount})
        return state_output

    @staticmethod
    def parse_application_state(
        application_state: Dict[str, Union[str, int]]
    ) -> ApplicationStateOutput:
        # Pact farms have no application state
        state_output: ApplicationStateOutput = {
            "asset_balances": dict(),
            "timestamp_from": None,
            "timestamp_to": None,
            "round_from": None,
            "round_to": None,
        }
        return state_output

    @staticmethod
    def test_application_type() -> bool:
        test_wallets = {
            "JTJ5JVY75TH2SILVAJU4SQRRY2XWEIT6VKTEQMII3QTXZVNT3RWUGUKFSA": {
                "asset_balances": {1076332142: 10119840, 1073557313: 1147547}
            }
        }

        for wallet, expected_result in test_wallets.items():
            res = test_application_type(wallet, PactFarm)
            print(res, expected_result)
            if res != expected_result:
                return False

        return True


if __name__ == "__main__":
    PactFarm.test_application_type()
