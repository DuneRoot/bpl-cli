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
        NetworkInterface.use(NetworkConfig.get_peer())

        secret_passphrase = Mnemonic("english").generate(256)

        account = SortedDictionary({
            "secret passphrase": secret_passphrase,
            "private key": Keys(secret_passphrase).get_private_key(),
            "public key": Keys(secret_passphrase).get_public_key(),
            "address": Address.from_secret(secret_passphrase)
        })

        print("\nAccount")
        print(Table([account.headers(), account.values()]))
