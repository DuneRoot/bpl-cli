import sys

from ascii_table import Table
from bpl_api import Client

from bpl_client.helpers.Exceptions import BPLClientNetworkException
from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.commands.Command import Command


class Peers(Command):

    def run(self):
        """
        Run method for network peers command.
        Fetches peers from peer using bpl_api.
        If request is unsuccessful then a BPLClientNetworkException is raised.
        Otherwise filter peers based on response status of peers and
        then display the filtered peers using an ascii_table.Table object.

        :return: (None)
        """

        peers = Client(NetworkConfig.get_peer()).api("peers").all_peers(limit=100)

        if not peers["success"]:
            print(BPLClientNetworkException({
                "message": "cannot get peers from network",
                "error": peers["error"]
            }), file=sys.stderr)
            sys.exit(1)

        filtered_peers = sorted(map(lambda x: "{0}:{1}".format(x["ip"], x["port"]), filter(
            lambda x: x["status"] == "OK", peers["peers"]
        )))

        print("\nPeers (Seed Peer: {0})".format(NetworkConfig.get_peer()))
        print(Table([{
            "Header": "Peers",
            "Contents": filtered_peers
        }]))
