import json
import sys

from ascii_table import Table

from bpl_client.commands.Command import Command
from bpl_client.helpers.Exceptions import BPLClientNetworkException
from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.helpers.Constants import NETWORK_CONFIG
from bpl_client.helpers.Util import write_file, SortedDictionary


class Use(Command):

    def run(self):
        """
        Run method for network config use command.
        Prints out a table of valid config identifiers.
        User is then prompted to input the name of a valid config identifier. If input is invalid a
        BPLClientNetworkException is raised. Otherwise the identifier is written to config.json and the new selected
        config is displayed using a ascii_table.Table object.

        :return: (None)
        """


        print("\nConfig Identifiers")
        print(Table([{
            "Header": "Configs",
            "Contents": NetworkConfig.get_config_identifiers()
        }]))

        config_identifier = input("\nEnter config identifier: ")

        if not NetworkConfig.validate_identifier(config_identifier):
            print(BPLClientNetworkException({
                "message": "invalid config identifier",
                "identifiers": NetworkConfig.get_config_identifiers(),
                "identifier": config_identifier
            }), file=sys.stderr)
            sys.exit(1)

        write_file(NETWORK_CONFIG, json.dumps({
            "identifier": config_identifier
        }))

        config = SortedDictionary(NetworkConfig.get_config())
        print("\nNetwork Config ({0})".format(config_identifier))
        print(Table([config.names(), config.values()]))
