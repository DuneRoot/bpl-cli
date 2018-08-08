from getpass import getpass

from bpl_lib.network import Network as NetworkInterface
from bpl_lib.crypto import Signature, sha256
from bpl_lib.address import Address
from ascii_table import Table

from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.helpers.Util import SortedDictionary
from bpl_client.commands.Command import Command


class Sign(Command):

    def __init__(self, arguments):
        """
        Message sign command constructor
        Initializes _message

        :param arguments: Contains list of arguments parsed from docopt (list)
        """

        super().__init__(arguments)
        self._message = sha256(self._arguments["<message>"].encode())

    def run(self):
        """
        Run method for message sign command
        Prints prompt for the user to enter secret passphrase (input is masked).
        Uses bpl_lib.crypto.Signature to sign message.
        Then displays the result using a ascii_table.Table object.

        :return: (None)
        """

        NetworkInterface.use(NetworkConfig.get_peer())

        secret_passphrase = getpass(prompt="Enter secret passphrase: ")

        signature = Signature(secret_passphrase).sign(self._message)
        signature = SortedDictionary({
            "public key": signature["public_key"],
            "address": Address.from_public_key(signature["public_key"]),
            "signature": signature["signature"]
        })

        print("\nSigned Message (Message: {0})".format(self._arguments["<message>"]))
        print(Table([signature.names(), signature.values()]))
