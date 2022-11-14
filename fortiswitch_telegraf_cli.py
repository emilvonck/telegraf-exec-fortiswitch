"""Cli for return data to Telegraf."""
from typing import Type

import typer

from fortiswitch import FortiSwitch

app = typer.Typer()


def enrich_dictionary(fortiswitch_obj: Type[FortiSwitch], data: dict):
    """Enrich dictionary with hostname and serial number, will be parsed as tags in InfluxDB.

    Args:
        fortiswitch_obj (Type[FortiSwitch]): Fortiswitch object.
        data (dict): Dictionary to enrich.
    """
    data.update(
        {
            "hostname": fortiswitch_obj.hostname,
            "serial_number": fortiswitch_obj.serial_number,
        }
    )


@app.command()
def get_switch_poe_sum(
    host: str, username: str, password: str, ssl_verify: bool = typer.Argument(True)
):
    """Cli command to get Swith PoE summary.

    Args:
        host (str): IP/DNS for the FortiSwitch API.
        username (str): Username for the FortiSwitch API.
        password (str): Password for the FortiSwitch API.
        ssl_verify (bool, optional): Whether to verify the SSL certificate presentet from the FortiSwitch API or not. Defaults to typer.Argument(True).
    """
    switch = FortiSwitch(
        host=host, username=username, password=password, verify=ssl_verify
    )

    original_interface_data = switch.get_switch_poe_sum()
    interface_list = []
    for interface_dict in original_interface_data:
        enrich_dictionary(switch, interface_dict)
        interface_list.append(interface_dict)

    return_data = {"poe_sum_list": interface_list}

    print(return_data)


if __name__ == "__main__":
    app()
