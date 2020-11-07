from icinga2api.client import Client
import argparse
import json

#Temp until certs enabled
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def parse_args():
    parser = argparse.ArgumentParser(description="Icinga config publisher",)
    parser.add_argument(
        "--type", dest="type", help="type, (Host, Service)", required=True
    )
    parser.add_argument(
        "--name", dest="name", help="Name of the object", required=True
    )
    parser.add_argument(
        "--template", dest="template", help="Template to use", nargs="+"
    )
    parser.add_argument(
        "--address", dest="address", help="Address", required=True
    )
    return parser.parse_args()

with open('secrets/icinga-api.json') as f:
  data = json.load(f)

icinga = Client(data['baseUrl'], data['user'], data['password'])

args     = parse_args()

fnret = icinga.objects.create(
    args.type,
    args.name,
    args.template,
    {'address':args.address}
)
print(fnret)