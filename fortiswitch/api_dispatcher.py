from fortiswitch.core import login
from fortiswitch.monitor import get_poe_status, get_port_state

API_GET_MAPPING = {
    "port": get_port_state,
    "poe-status": get_poe_status,
}

endpoints = list(API_GET_MAPPING.keys())
endpoints.sort()
endpoints_str = "\n".join(endpoints)


def GetHandler(endpoint: str, **kwargs):
    if endpoint not in endpoints:
        raise ValueError(f"Currently supported endpoints are: {endpoints_str}")
    session = login(**kwargs)
    return API_GET_MAPPING[endpoint](session)
