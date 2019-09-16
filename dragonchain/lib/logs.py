import os
import json
from typing import List, Dict, Optional, cast, Any

import requests

from dragonchain.lib.faas import get_faas_auth

FAAS_GATEWAY = os.environ["FAAS_GATEWAY"]


def get_raw_logs(contract_id: str, since: Optional[str] = None, tail: Optional[int] = 100) -> List[str]:
    """Calls openfaas /system/logs endpoint with query parameters for a specific contract"""
    endpoint = f"{FAAS_GATEWAY}/system/logs"
    query_params = cast(Dict[str, Any], {"name": f"contract-{contract_id}", "tail": tail, "since": since})
    response = requests.get(endpoint, params=query_params, headers={"Authorization": get_faas_auth()})
    if response.status_code != 200:
        raise RuntimeError("Error getting contract logs, non-2XX response from OpenFaaS gateway")

    return response.text.split("\n")


def get_logs(contract_id: str, since: Optional[str] = None, tail: Optional[int] = 100) -> List[Dict[str, str]]:
    """Gets the raw logs from openfaas and parses the ndjson into a list of dictionaries"""
    raw_logs = get_raw_logs(contract_id, since, tail)
    return list(map(lambda x: json.parse(x), raw_logs))
