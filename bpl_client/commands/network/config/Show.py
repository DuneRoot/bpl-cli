from ascii_table import Table

from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.helpers.Util import SortedDictionary
from bpl_client.commands.Command import Command


class Show(Command):

    def run(self):
        """
        Run method for network config show command.
        Reads the network config and then displays it in a ascii_table.Table object

        :return: (None)
        """

        config = SortedDictionary(NetworkConfig.get_config())

        print("\nNetwork Config ({0})".format(NetworkConfig.get_config_identifier()))
        print(Table([config.names(), config.values()]))

