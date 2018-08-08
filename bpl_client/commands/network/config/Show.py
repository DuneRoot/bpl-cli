from ascii_table import Table

from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.helpers.Util import SortedDictionary
from bpl_client.commands.Command import Command


class Show(Command):

    def run(self):
        config = SortedDictionary(NetworkConfig.get_config())

        print("\nNetwork Config")
        print(Table([config.headers(), config.values()]))

