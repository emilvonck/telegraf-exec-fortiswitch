# noqa: D100
import argparse

from fortiswitch import GetHandler

my_parser = argparse.ArgumentParser(
    prog="fortiswitch_app",
    usage="%(prog)s [options]",
    description="Fetch data from FortiSwitch API",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)


my_parser.add_argument(
    "--host", type=str, help="Host for API connection", required=True
)
my_parser.add_argument(
    "--port", type=int, help="Destination port for API connection", default=443
)
my_parser.add_argument(
    "--username", type=str, help="Username for the Host", required=True
)
my_parser.add_argument(
    "--password", type=str, help="Password for the Host", required=True
)
my_parser.add_argument("--endpoint", type=str, help="API endpoint", required=True)
my_parser.add_argument(
    "--ignore_ssl", action="store_false", help="Skip SSL verification"
)

args = my_parser.parse_args()

data = GetHandler(**vars(args))
print(data)
