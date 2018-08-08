from getpass import getpass

from bpl_api import Client
from bpl_lib.network import Network as NetworkInterface
from bpl_lib.transactions import Delegate as DelegateTransaction

from bpl_client.commands.Command import Command
from bpl_client.network.NetworkConfig import NetworkConfig


class Delegate(Command):

    def __init__(self, arguments):
        super().__init__(arguments)
        self._username = self._arguments["<username>"]

    def run(self):
        bpl_transactions = Client(NetworkConfig.get_peer()).api("transactions")
        NetworkInterface.use(NetworkConfig.get_peer())

        #secret_passphrase = input("Enter secret passphrase: ")
        secret_passphrase = getpass(prompt="Enter secret passphrase: ")

        if input("confirm (y/n): ").lower() not in ["y", "yes"]:
            print("Aborted.")
            return

        transaction = DelegateTransaction.generate(self._username, secret_passphrase).to_dict()
        response = bpl_transactions.send(transaction)

        if response["success"]:
            print("Transaction sent successfully with id {0}.".format(transaction["id"]))
        else:
            print("Failed to send transaction: {0}.".format(response["error"]))
