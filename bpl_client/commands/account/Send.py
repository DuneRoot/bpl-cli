from getpass import getpass

from bpl_lib.network import Network as NetworkInterface
from bpl_lib.transactions import Transfer
from bpl_api import Client

from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.commands.Command import Command
from bpl_client.helpers.Constants import BPL


class Send(Command):

    def __init__(self, arguments):
        """
        Account send command constructor
        Initializes _recipient_id and _amount

        :param arguments: Contains list of arguments parsed from docopt (list)
        """

        super().__init__(arguments)
        self._recipient_id = self._arguments["<recipient>"]
        self._amount = int(float(self._arguments["<amount>"]) * BPL)

    def run(self):
        """
        Run method for account send command.
        The user is prompted for the secret passphrase (input is masked).
        Then the user must confirm the transaction. If the user aborts the transaction then "Aborted." is printed and
        the transaction isn't sent.
        Otherwise the transaction is constructed using bpl_lib.transactions.Transfer and sent using bpl_api.
        Then "Sending x BPL to y" is displayed.
        If the transaction is successful then "Transaction sent successfully with id x" is displayed, otherwise
        "Failed to sent transaction: x" is displayed.

        :return: (None)
        """

        bpl_transactions = Client(NetworkConfig.get_peer()).api("transactions")
        NetworkInterface.use(NetworkConfig.get_peer())

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
