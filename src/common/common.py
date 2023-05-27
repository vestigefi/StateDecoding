import requests
import json
import base64
from typing import Dict, Union, List, Callable
from algosdk.abi import ABIType
from .abstract import RawWalletState, ApplicationType, WalletStateOutput
from collections import defaultdict


MAINNET_NODE_API_URL = "https://mainnet-api.algonode.cloud/"
MAINNET_INDEXER_API_URL = "https://mainnet-idx.algonode.cloud/"


def get_request(url: str, allow_codes=None) -> dict:
    """
    Send a GET request to a JSON endpoint url

    Args:
        url (str): endpoint address
        allow_codes (list): http codes allowed in response

    Raises:
        Exception: when request fails

    Returns:
        dict: JSON data
    """
    if allow_codes is None:
        allow_codes = []
    response = requests.get(url)
    if not response.ok and response.status_code not in allow_codes:
        raise Exception("Failed GET request: {}".format(url))
    else:
        return json.loads(response.content)


def node_get_request(endpoint: str, allow_codes=None) -> dict:
    """
    Send a GET request to Algorand Node API endpoint

    Args:
        endpoint (str): endpoint suffix
        allow_codes (list): http codes allowed in response

    Raises:
        Exception: when request fails

    Returns:
        dict: JSON data
    """
    return get_request(f"{MAINNET_NODE_API_URL}{endpoint}", allow_codes)


def indexer_get_request(endpoint: str, allow_codes=None) -> dict:
    """
    Send a GET request to a JSON endpoint url

    Args:
        endpoint (str): endpoint address
        allow_codes (list): http codes allowed in response

    Raises:
        Exception: when request fails

    Returns:
        dict: JSON data
    """
    return get_request(f"{MAINNET_INDEXER_API_URL}{endpoint}", allow_codes)


def state_entry_to_dict(state_entry: dict) -> Dict[str, Union[str, int]]:
    """Format JSON state entry into dict"""
    state_dict = dict()
    value_state = state_entry.get("value", dict())
    value_bytes = value_state.get("bytes", None)
    state_dict[state_entry.get("key", "ERR")] = (
        value_bytes if value_bytes else value_state.get("uint", None)
    )
    return state_dict


def get_application_state(application_id: int) -> Dict[str, Union[str, int]]:
    """Returns application state as dict (MEANT TO BE USED FOR TESTS ONLY)"""
    try:
        state = dict()
        data = indexer_get_request(f"v2/applications/{application_id}")
        application = data.get("application")
        params = application.get("params")
        local_state = params.get("local-state")
        global_state = params.get("global-state")
        if global_state:
            for entry in global_state:
                state.update(state_entry_to_dict(entry))
        if local_state:
            for wallet_state in local_state:
                for entry in wallet_state.get("delta", []):
                    # TODO: Can't put both local and global state into the dict like this
                    # as they might have the same keys.
                    state.update(state_entry_to_dict(entry))
        return state
    except Exception as e:
        raise Exception(f"Couldn't view application state for ID {application_id}: {e}")


def get_wallet_state(address: str) -> RawWalletState:
    """Returns wallet state for application as dict (MEANT TO BE USED FOR TESTS ONLY)"""
    try:
        wallet_state = {"assets": dict(), "local_state": dict(), "created_apps": dict()}
        data = indexer_get_request(f"v2/accounts/{address}")
        account = data.get("account")

        # Get assets with non-zero values
        for asset in account.get("assets"):
            amount = asset.get("amount")
            id = asset.get("asset-id")
            if amount and id:
                wallet_state["assets"].update({id: amount})

        # Get local state per app, as key:value pairs.
        for application in account.get("apps-local-state", []):
            state_values = dict()
            for state in application.get("key-value"):
                id = application.get("id")
                state_value = state.get("value")
                b = state_value.get("bytes")
                i = state_value.get("uint")
                state_values.update({state.get("key"): i if i else b})
            wallet_state["local_state"].update({id: state_values})

        # Get created apps, their IDs and their bytecodes
        for created_application in account.get("created-apps", []):
            if created_application.get("deleted"):
                continue
            id = created_application.get("id")
            bytecode = created_application.get("params").get("approval-program")
            wallet_state["created_apps"].update({id: bytecode})
        return wallet_state
    except Exception as e:
        raise Exception(f"Couldn't view wallet state for address {address}: {e}")


def test_application_type(
    wallet: str, application_type: ApplicationType
) -> WalletStateOutput:
    result = defaultdict(lambda: 0)
    static_application_ids = application_type.fetch_static_application_ids()
    dynamic_application_ids = application_type.fetch_dynamic_application_ids(0)

    # Get account state
    response = node_get_request(f"v2/accounts/{wallet}")
    wallet_apps = response.get("apps-local-state")
    wallet_application_ids = [app.get("id") for app in wallet_apps]
    raw_wallet_state = get_wallet_state(wallet)

    app_application_ids = list(set(static_application_ids + dynamic_application_ids))

    # For each application, get it's state, use it to parse the wallet state and add the asset amounts to the result
    for application_id in wallet_application_ids:
        if application_id not in app_application_ids:
            continue

        raw_app_state = get_application_state(application_id)
        if not application_type.is_application_state_valid(raw_app_state):
            continue
        app_state = application_type.parse_application_state(
            get_application_state(application_id)
        )

        if not application_type.is_wallet_state_valid(raw_wallet_state, application_id):
            continue

        wallet_state = application_type.parse_wallet_state(
            raw_wallet_state, app_state, application_id
        )
        asset_balances = wallet_state.get("asset_balances")
        for asset, amount in asset_balances.items():
            result[asset] += amount
    return {"asset_balances": dict(result)}


def base64_state_to_bytes(keys: List[str], state: Dict[str, Union[str, int]]) -> bytes:
    """
    Parse base64-encoded values from state dict to bytes (for compressed memory SCs)

    Args:
        keys (list): ordered list of keys to be concatenated together
        state (dict): dict containing state keys

    Returns:
        bytes: bytes of SC memory
    """
    state_bytes = b""
    for key in keys:
        if type(state[key]) != str:
            raise Exception(f"Key {key} is not a string.")
        if key not in state:
            raise Exception(f"Key {key} not found in state.")
        try:
            state_bytes += base64.b64decode(state[key])
        except Exception as e:
            raise Exception(f"Key {key} is not a base64 valid string: {e}")
    return state_bytes


def state_bytes_to_values(ABI_string: str, state_bytes: bytes) -> list:
    """
    Get values from state memory bytes

    Args:
        ABI_string: valid ABI string describing bytes format
        state_bytes: bytes of memory to decode

    Returns:
        list: state values list
    """
    try:
        value = ABIType.from_string(ABI_string).decode(state_bytes)
        if type(value) == list:
            return value
        else:
            return [value]
    except Exception as e:
        raise Exception(f"Invalid ABI string or state bytes: {e}")
