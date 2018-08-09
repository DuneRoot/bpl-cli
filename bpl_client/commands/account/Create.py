from bpl_lib.network import Network as NetworkInterface
from bpl_lib.address import Address
from bpl_lib.crypto import Keys
from ascii_table import Table
from mnemonic import Mnemonic

from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.helpers.Util import SortedDictionary
from bpl_client.commands.Command import Command


class Create(Command):

    def run(self):
        """
        Run method for account create command
        Generates a secret passphrase using BIP39 mnemonic generator.
        Private and public keys are then calculated using bpl_lib.crypto.Keys and
        the address is generate from the secret passphrase using bpl_lib.address.Address.
        The secret passphrase, private key, public key and address are then displayed in a
        ascii_table.Table object.

        :return: (None)
        """

        NetworkInterface.use(NetworkConfig.get_config_identifier())

        secret_passphrase = Mnemonic("english").generate(256)

        account = SortedDictionary({
            "secret passphrase": secret_passphrase,
            "private key": Keys(secret_passphrase).get_private_key(),
            "public key": Keys(secret_passphrase).get_public_key(),
            "address": Address.from_secret(secret_passphrase)
        })

        print("\nAccount")
        print(Table([account.names(), account.values()]))
