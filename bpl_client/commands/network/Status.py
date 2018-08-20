import sys

from ascii_table import Table
from bpl_api import Client

from bpl_client.helpers.Exceptions import BPLClientNetworkException
from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.helpers.Util import SortedDictionary
from bpl_client.commands.Command import Command


class Status(Command):

    def run(self):
        """
        Run method of network status command.
        Fetches status of peer using bpl_api.
        If request is unsuccessful then a BPLClientNetworkException is raised.
        Otherwise display the status using an ascii_table.Table object

        :return: (None)
        """

        status = Client(NetworkConfig.get_peer()).api("blocks").status()

        if not status["success"]:
            print(BPLClientNetworkException({
                "message": "cannot get status from network",
                "error": status["error"]
            }), file=sys.stderr)
            sys.exit(1)

        status.pop("success", None)
        status["reward"] = status["reward"]["reward"]
        status = SortedDictionary(status)

        print("\nNetwork Summary")
        print(Table([status.names(), status.values()]))
