import re as regular_expression
from datetime import datetime
import json

from bpl_lib.helpers import BPLNetworkException
from bpl_lib.network import Network
from ascii_table import Table
from bpl_api import Client

from bpl_client.helpers.Constants import PEER_ADDRESS_REGEX, VERSION_REGEX, EPOCH_REGEX, NETWORK_CONFIG
from bpl_client.helpers.Exceptions import BPLClientNetworkException
from bpl_client.helpers.Util import write_file, SortedDictionary
from bpl_client.commands.Command import Command


class Setup(Command):

    def run(self):
        """
        Run method for network config setup command.
        Prints prompt requesting peer address and port, peer address user input is validated using a regular expression.
        A similar process is applied to the network version and begin epoch prompts.
        If validation fails at a given state then a BPLClientNetworkException is raised.
        Otherwise the nethash is fetch from the peer address the user entered and is stored in the network config json
        file. The config is then displayed using a ascii_table.Table object

        :return: (None)
        """

        peer_address = input("Enter peer address and port: ")

        if not regular_expression.match(PEER_ADDRESS_REGEX, peer_address):
            raise BPLClientNetworkException({
                "message": "invalid peer address.",
                "format": "[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:[0-9]{1,5}",
                "peer": peer_address
            })

        version = input("Enter version: ")

        if not regular_expression.match(VERSION_REGEX, version):
            raise BPLClientNetworkException({
                "message": "invalid network version.",
                "format": "[0-9]{1,3}",
                "version": version
            })

        begin_epoch = input("Enter begin epoch: ")

        if not regular_expression.match(EPOCH_REGEX, begin_epoch):
            raise BPLClientNetworkException({
                "message": "invalid begin epoch.",
                "format": "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}",
                "begin epoch": begin_epoch
            })

        try:
            nethash = Client(peer_address).api("blocks").nethash()["nethash"]
        except:
            raise BPLClientNetworkException({
                "message": "failed to fetch nethash.",
                "reason": "failed to successfully connect to peer."
            })

        config = {
            "peer address": peer_address,
            "version": int(version),
            "begin epoch": begin_epoch,
            "nethash": nethash
        }

        write_file(NETWORK_CONFIG, json.dumps(config))

        try:
            Network.use_custom(
                peer_address, datetime.strptime(config["begin epoch"], "%Y-%m-%d %H:%M:%S"), config["version"]
            )
        except BPLNetworkException:
            pass

        config = SortedDictionary(config)
        print("\nNetwork Config")
        print(Table([config.names(), config.values()]))
