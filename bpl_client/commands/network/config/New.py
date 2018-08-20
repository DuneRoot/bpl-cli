import re as regular_expression
from datetime import datetime
import json
import sys

from bpl_lib.helpers import BPLNetworkException
from bpl_lib.network import Network
from ascii_table import Table
from bpl_api import Client

from bpl_client.helpers.Constants import PEER_ADDRESS_REGEX, VERSION_REGEX, EPOCH_REGEX, NETWORK_CONFIG, NETWORK_CONFIGS
from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.helpers.Exceptions import BPLClientNetworkException
from bpl_client.helpers.Util import write_file, SortedDictionary
from bpl_client.commands.Command import Command


class New(Command):

    def run(self):
        """
        Run method for network config new command.
        Prints prompt requesting config identifier.
        Prints prompt requesting peer address and port, peer address user input is validated using a regular expression.
        A similar process is applied to the network version and begin epoch prompts.
        If validation fails at a given state then a BPLClientNetworkException is raised.
        Otherwise the nethash is fetch from the peer address the user entered.
        The currently used config identifier is then stored in config.json and the new config is stored in configs.json
        file. The config is then displayed using a ascii_table.Table object

        :return: (None)
        """

        config_identifier = input("Enter config identifier: ")

        if NetworkConfig.validate_identifier(config_identifier):
            print(BPLClientNetworkException({
                "message": "invalid config identifier. config identifier has already been used.",
                "config identifiers": NetworkConfig.get_config_identifiers(),
                "config identifier": config_identifier
            }), file=sys.stderr)
            sys.exit(1)

        peer_address = input("Enter peer address and port: ")

        if not regular_expression.match(PEER_ADDRESS_REGEX, peer_address):
            print(BPLClientNetworkException({
                "message": "invalid peer address.",
                "format": "[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:[0-9]{1,5}",
                "peer": peer_address
            }), file=sys.stderr)
            sys.exit(1)

        version = input("Enter version: ")

        if not regular_expression.match(VERSION_REGEX, version):
            print(BPLClientNetworkException({
                "message": "invalid network version.",
                "format": "[0-9]{1,3}",
                "version": version
            }), file=sys.stderr)
            sys.exit(1)

        begin_epoch = input("Enter begin epoch: ")

        if not regular_expression.match(EPOCH_REGEX, begin_epoch):
            print(BPLClientNetworkException({
                "message": "invalid begin epoch.",
                "format": "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}",
                "begin epoch": begin_epoch
            }), file=sys.stderr)
            sys.exit(1)

        try:
            nethash = Client(peer_address).api("blocks").nethash()["nethash"]
        except:
            print(BPLClientNetworkException({
                "message": "failed to fetch nethash.",
                "reason": "failed to successfully connect to peer."
            }), file=sys.stderr)
            sys.exit(1)

        configs = NetworkConfig.get_configs()
        configs[config_identifier] = {
            "peer address": peer_address,
            "version": int(version),
            "begin epoch": begin_epoch,
            "nethash": nethash
        }

        write_file(NETWORK_CONFIG, json.dumps({
            "identifier": config_identifier
        }))
        write_file(NETWORK_CONFIGS, json.dumps(configs))

        try:
            Network.use_custom(
                config_identifier, datetime.strptime(begin_epoch, "%Y-%m-%d %H:%M:%S"), int(version)
            )
        except BPLNetworkException:
            pass

        config = SortedDictionary(configs[config_identifier])
        print("\nNetwork Config ({0})".format(config_identifier))
        print(Table([config.names(), config.values()]))
