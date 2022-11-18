"""Cli for printing json strings from data returned by FortiSwitch class methods."""
import argparse
import json
import os
import sys
from typing import Dict, List, Type, Union

from fortiswitch import FortiSwitch
from fortiswitch.utils import LogHandler

FILE_NAME = os.path.basename(__file__).strip(".py")

logging = LogHandler(FILE_NAME)

METHOD_LIST = [
    func
    for func in dir(FortiSwitch)
    if callable(getattr(FortiSwitch, func))
    and not func.startswith("__")  # noqa: W503
    and not func.startswith("_")  # noqa: W503
]


def _enrich_return_data(
    fortiswitch_obj: Type[FortiSwitch], data: Union[List[Dict], Dict]
):
    if isinstance(data, dict):
        data.update(
            {
                "serial": fortiswitch_obj.serial_number,
                "hostname": fortiswitch_obj.hostname,
            }
        )
    if isinstance(data, list):
        for i in data:
            if isinstance(i, dict):
                i.update(
                    {
                        "serial": fortiswitch_obj.serial_number,
                        "hostname": fortiswitch_obj.hostname,
                    }
                )
    return data


def _make_fortiswitch(host, username, password, verify, **kwargs) -> FortiSwitch:
    try:
        return FortiSwitch(host, username, password, verify)
    except Exception as err:
        logging_dict = {
            "level": 40,
            "message_type": "make_fortiswitch",
            "failed_host": host,
            "message": str(err),
        }
        logging.format_logs(**logging_dict)
        sys.exit(1)


def _endpoint_dispatcher(fortiswitch_obj: Type[FortiSwitch], cls_method: str):
    if cls_method not in METHOD_LIST:
        logging_dict = {
            "level": 40,
            "message_type": "endpoint_dispatcher",
            "message": "Unsupported 'cls_method",
            "given_method": cls_method,
            "supported_methods": METHOD_LIST,
        }
        logging.format_logs(**logging_dict)
        sys.exit(1)

    index = METHOD_LIST.index(cls_method)
    method = getattr(FortiSwitch, METHOD_LIST[index])

    return method(fortiswitch_obj)


def cli_call(host, username, password, ignore_ssl, cls_method, **kwargs) -> None:
    """Instantiate FortiSwitch and prints returned data as a json string.

    Args:
        host (_type_): FortiSwitch API host.
        username (_type_): FortiSwitch username.
        password (_type_): FortiSwitch password.
        ignore_ssl (_type_): Whether to vaildate SSL certificates or not.
        cls_method (_type_): FortiSwitch class method.
    """
    switch_kwargs = {
        "host": host,
        "username": username,
        "password": password,
        "verify": ignore_ssl,
    }
    switch = _make_fortiswitch(**switch_kwargs)
    original_data = _endpoint_dispatcher(switch, cls_method)
    return_data = {cls_method: _enrich_return_data(switch, original_data)}

    print(json.dumps(return_data))


my_parser = argparse.ArgumentParser(
    prog=FILE_NAME,
    usage="%(prog)s [options]",
    description="Fetch data from FortiSwitch API",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

my_parser.add_argument("--host", type=str, help="FortiSwitch API host.", required=False)
my_parser.add_argument(
    "--port", type=int, help="Destination port for FortiSwitch API host", default=443
)
my_parser.add_argument(
    "--username", type=str, help="FortiSwitch username.", required=False
)
my_parser.add_argument(
    "--password", type=str, help="FortiSwitch password.", required=False
)
my_parser.add_argument(
    "--cls_method", type=str, help="FortiSwitch class method.", required=True
)
my_parser.add_argument(
    "--ignore_ssl", action="store_false", help="Skip SSL certificate verification."
)
args = my_parser.parse_args()

if os.environ.get("FORTISWITCH_HOST"):
    args.host = os.environ.get("FORTISWITCH_HOST")

if os.environ.get("FORTISWITCH_USER"):
    args.username = os.environ.get("FORTISWITCH_USER")

if os.environ.get("FORTISWITCH_PASS"):
    args.password = os.environ.get("FORTISWITCH_PASS")

missing_args = [
    {k: v} for k, v in vars(args).items() if not v and not k == "ignore_ssl"
]

if missing_args:
    logging_dict = {
        "level": 40,
        "message_type": "missing_variables",
        "message": f"{len(missing_args)} variables are missing",
        "unset_variables": missing_args,
    }
    logging.format_logs(**logging_dict)
    sys.exit(1)

cli_call(**vars(args))
