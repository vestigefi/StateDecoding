import requests
import json
from typing import Dict, Union
from src.common.logger import logger


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
    """Returns application state as dict"""
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
                    state.update(state_entry_to_dict(entry))
        return state
    except Exception as e:
        logger.error(f"Couldn't view application state for ID {application_id}: {e}")
        return dict()
