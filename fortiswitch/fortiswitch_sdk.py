# noqa: D100
from sys import version as python_version
from typing import Dict, List

import requests
import urllib3

from fortiswitch.utils import LogHandler

logging = LogHandler(__name__)


class FortiSwitch:
    """Class for interacting with the FortiSwitchOS API."""

    def __init__(self, host: str, username: str, password: str, verify: bool = True):
        """Initializor for the class.

        Args:
            host (str): Host for the API, IP or DNSname.
            username (str): Username.
            password (str): Password.
            verify (bool, optional): Whether to verify SSL certificates or not. Defaults to True.
        """
        self.host = host
        self.username = username
        self.password = password
        self._verify = verify
        self.session = requests.Session()

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"Python {python_version.split(' ', maxsplit=1)[0]}",
        }

        self._monitor_base_url = "api/v2/monitor"
        self._property_extractors()

    @property
    def verify(self):
        # noqa: D102
        return self._verify

    @verify.setter
    def verify(self, value: bool):
        # noqa: D102
        if not isinstance(value, bool):
            raise TypeError(f"invalid type for '{value}' must be of type {type(True)}")
        else:
            self._verify = value

    @property
    def hostname(self):
        # noqa: D102
        return self._get_system_status()["hostname"]

    @property
    def burn_in_mac(self):
        # noqa: D102
        return self._system_status["burn_in_mac"]

    @property
    def serial_number(self):
        # noqa: D102
        return self._system_status["serial_number"]

    @property
    def model(self):
        # noqa: D102
        return self._capabilities["results"]["fortiswitch"][0]["system-info"]["model"]

    @property
    def system_part_number(self):
        # noqa: D102
        return self._system_status["system_part_number"]

    @property
    def os_version(self):
        # noqa: D102
        return self._get_switch_capabilities()["version"]

    @property
    def os_version_build(self):
        # noqa: D102
        return self._get_switch_capabilities()["build"]

    @property
    def bios_version(self):
        # noqa: D102
        return self._get_switch_capabilities()["results"]["fortiswitch"][0][
            "system-info"
        ]["bios-version"]

    def _property_extractors(self):
        # noqa: D102
        extractors = {
            "system_status": self._get_system_status(),
            "capabilities": self._get_switch_capabilities(),
        }

        for k, v in extractors.items():
            setattr(self, f"_{k}", v)

    def _login(self):
        base_url = "login"
        url = f"https://{self.host}/{base_url}"

        data = {
            "username": self.username,
            "password": self.password,
        }

        self._req(url=url, method="post", body=data)

    def _logout(self):
        base_url = "logout"
        url = f"https://{self.host}/{base_url}"

        self._req(url=url, method="post")

    def _req(self, url, method="get", params=None, body=None):

        logging_dict = {
            "message_type": f"http {method}",
            "url": url,
        }

        if not self.verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        response = self.session.request(
            url=url, data=body, params=params, method=method, verify=self.verify
        )

        if response:
            level = 20
            logging_dict.update(
                {
                    "message": response.reason,
                    "status_code": response.status_code,
                    "level": level,
                    "response_url": response.url,
                }
            )

        else:
            level = 30
            logging_dict.update(
                {
                    "message": response.reason,
                    "status_code": response.status_code,
                    "level": level,
                    "response_url": response.url,
                }
            )

        logging.format_logs(**logging_dict)

        return response

    def _get_system_status(self) -> dict:
        self._login()
        base_url = "system/status"
        url = f"https://{self.host}/{self._monitor_base_url}/{base_url}"

        result = self._req(url=url, method="get")
        self._logout()

        return result.json()["results"]

    def _get_switch_capabilities(self):
        self._login()
        base_url = "switch/capabilities"
        url = f"https://{self.host}/{self._monitor_base_url}/{base_url}"

        result = self._req(url=url, method="get")
        self._logout()

        return result.json()

    def get_switch_port_state(self) -> List[Dict]:
        # noqa: D102
        self._login()
        base_url = "switch/port"
        url = f"https://{self.host}/{self._monitor_base_url}/{base_url}"

        result = self._req(url=url, method="get")
        self._logout()

        interface_list = []
        for _, interface_property in result.json()["results"].items():
            interface_property.update({"interface": interface_property["name"]})
            interface_property.pop("name")
            interface_list.append(interface_property)

        return interface_list

    def get_switch_port_statistics(self):
        # noqa: D102
        self._login()
        base_url = "switch/port-statistics"
        url = f"https://{self.host}/{self._monitor_base_url}/{base_url}"

        result = self._req(url=url, method="get")
        self._logout()

        interface_list = []
        for interface_name, interface_property in result.json()["results"].items():
            interface_property.update({"interface": interface_name})
            interface_list.append(interface_property)

        return interface_list

    def _get_switch_poe_status(self) -> List:
        # noqa: D102
        self._login()
        base_url = "switch/poe-status"
        url = f"https://{self.host}/{self._monitor_base_url}/{base_url}"

        result = self._req(url=url, method="get")
        self._logout()

        return result.json()["results"]

    def get_system_poe_status(self) -> Dict:
        # noqa: D102
        system_poe_status = self._get_switch_poe_status()[0]

        return {k.lower(): v for k, v in system_poe_status.items()}

    def get_switch_poe_status(self) -> List[Dict]:
        # noqa: D102
        switch_poe_status = self._get_switch_poe_status()
        interface_poe_status = [i for i in switch_poe_status if i.get("Interface")]
        interface_poe_status_return = []

        for interface in interface_poe_status:
            interface = {k.lower(): v for k, v in interface.items()}
            interface_poe_status_return.append(interface)

        return interface_poe_status_return

    def _get_system_resource(self) -> Dict:
        # noqa: D102
        self._login()
        base_url = "system/resource"
        url = f"https://{self.host}/{self._monitor_base_url}/{base_url}"

        result = self._req(url=url, method="get")
        self._logout()

        return result.json()["results"]

    def get_system_cpu_usage(self):
        # noqa: D102
        cpu_usage = self._get_system_resource()["cpu"][0]

        return {"cpu_usage": cpu_usage}

    def get_system_mem_usage(self):
        # noqa: D102
        mem_usage = self._get_system_resource()["mem"]

        return {"mem_usage": mem_usage}

    def get_system_psu_status(self):
        # noqa: D102
        self._login()
        base_url = "system/psu-status"
        url = f"https://{self.host}/{self._monitor_base_url}/{base_url}"

        result = self._req(url=url, method="get")
        self._logout()

        return result.json()["results"]

    def get_system_fan_status(self):
        # noqa: D102
        self._login()
        base_url = "system/fan-status"
        url = f"https://{self.host}/{self._monitor_base_url}/{base_url}"

        result = self._req(url=url, method="get")
        self._logout()

        return result.json()["results"]

    def get_system_pcb_temp(self):
        # noqa: D102
        self._login()
        base_url = "system/pcb-temp"
        url = f"https://{self.host}/{self._monitor_base_url}/{base_url}"

        result = self._req(url=url, method="get")
        self._logout()

        temp_modules = []
        for module in result.json()["results"]:
            module.update(
                {
                    "value": module["status"]["value"],
                    "unit": module["status"]["unit"],
                }
            )
            module.pop("status")
            temp_modules.append(module)

        return temp_modules

    def get_system_upgrade_status(self):
        # noqa: D102
        self._login()
        base_url = "system/upgrade-status"
        url = f"https://{self.host}/{self._monitor_base_url}/{base_url}"

        result = self._req(url=url, method="get")
        self._logout()

        return result.json()["results"]

    def get_switch_properties(self) -> dict:
        # noqa: D102
        PROPERTY_LIST = [
            prop
            for prop in dir(FortiSwitch)
            if not callable(getattr(FortiSwitch, prop))
            and not prop.startswith("__")  # noqa: W503
            and not prop.startswith("_")  # noqa: W503
        ]

        return {i: getattr(self, i) for i in PROPERTY_LIST}
