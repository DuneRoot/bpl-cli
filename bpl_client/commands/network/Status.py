from ascii_table import Table
from bpl_api import Client

from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.helpers.Util import SortedDictionary
from bpl_client.commands.Command import Command


class Status(Command):

    def run(self):
        status = Client(NetworkConfig.get_peer()).api("blocks").status()

        status["reward"] = status["reward"]["reward"]
        status.pop("success", None)
        status = SortedDictionary(status)

        print("\nNetwork Summary")
        print(Table([status.headers(), status.values()]))
