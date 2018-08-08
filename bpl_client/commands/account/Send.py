from getpass import getpass

from bpl_api import Client
from bpl_lib.network import Network as NetworkInterface
from bpl_lib.transactions import Transfer

from bpl_client.commands.Command import Command
from bpl_client.helpers.Constants import BPL
from bpl_client.network.NetworkConfig import NetworkConfig


class Send(Command):

    def __init__(self, arguments):
        super().__init__(arguments)
        self._recipient_id = self._arguments["<recipient>"]
        self._amount = int(float(self._arguments["<amount>"]) * BPL)

    def run(self):
        bpl_transactions = Client(NetworkConfig.get_peer()).api("transactions")
        NetworkInterface.use(NetworkConfig.get_peer())


        #secret_passphrase = input("Enter secret passphrase: ")
        secret_passphrase = getpass(prompt="Enter secret passphrase: ")

        if input("Confirm (y/n): ").lower() not in ["y", "yes"]:
            print("Aborted.")
            return

        transaction = Transfer.generate(self._recipient_id, self._amount, secret_passphrase).to_dict()

        print("Sending {0} BPL to {1}.".format(self._arguments["<amount>"], self._recipient_id))
        response = bpl_transactions.send(transaction)

        if response["success"]:
            print("Transaction sent successfully with id {0}.".format(transaction["id"]))
        else:
            print("Failed to send transaction: {0}.".format(response["error"]))
