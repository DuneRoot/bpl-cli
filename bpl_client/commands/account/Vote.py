from getpass import getpass

from bpl_api import Client
from bpl_lib.network import Network as NetworkInterface
from bpl_lib.transactions import Vote as VoteTransaction

from bpl_client.commands.Command import Command
from bpl_client.helpers.Exceptions import BPLClientAccountsException
from bpl_client.network.NetworkConfig import NetworkConfig


class Vote(Command):

    def __init__(self, arguments):
        super().__init__(arguments)
        self._username = self._arguments["<username>"]

    def run(self):
        bpl_transactions = Client(NetworkConfig.get_peer()).api("transactions")
        NetworkInterface.use(NetworkConfig.get_peer())

        if not self._verify_delegate():
            raise BPLClientAccountsException({
                "message": "Invalid delegate.",
                "delegate": self._username
            })

        votes = ["+" + self._get_public_key()]
        #secret_passphrase = input("Enter secret passphrase: ")
        secret_passphrase = getpass(prompt="Enter secret passphrase: ")

        if input("Confirm (y/n): ").lower() not in ["y", "yes"]:
            print("Aborted.")
            return

        transaction = VoteTransaction.generate(votes, secret_passphrase).to_dict()
        response = bpl_transactions.send(transaction)

        if response["success"]:
            print("Transaction sent successfully with id {0}.".format(transaction["id"]))
        else:
            print("Failed to send transaction: {0}.".format(response["error"]))

    def _verify_delegate(self):
        return Client(NetworkConfig.get_peer()).api("delegates").delegate(self._username)["success"]

    def _get_public_key(self):
        return Client(NetworkConfig.get_peer()).api("delegates").delegate(self._username)["delegate"]["publicKey"]
