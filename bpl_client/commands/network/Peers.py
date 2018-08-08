from ascii_table import Table
from bpl_api import Client

from bpl_client.helpers.Exceptions import BPLClientNetworkException
from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.commands.Command import Command


class Peers(Command):

    def run(self):
        peers = Client(NetworkConfig.get_peer()).api("peers").all_peers(limit=100)

        if not peers["success"]:
            raise BPLClientNetworkException({
                "message": "cannot get peers from network",
                "error": peers["error"]
            })

        filtered_peers = sorted(map(lambda x: "{0}:{1}".format(x["ip"], x["port"]), filter(
            lambda x: x["status"] == "OK", peers["peers"]
        )))

        print("\nPeers (Seed Peer: {0})".format(NetworkConfig.get_peer()))
        print(Table([{
            "Header": "Peers",
            "Contents": filtered_peers
        }]))
