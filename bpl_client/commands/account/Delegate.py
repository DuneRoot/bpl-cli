from getpass import getpass

from bpl_lib.transactions import Delegate as DelegateTransaction
from bpl_lib.network import Network as NetworkInterface
from bpl_api import Client

from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.commands.Command import Command


class Delegate(Command):

    def __init__(self, arguments):
        """
        Account delegate command constructor
        Initializes _username

        :param arguments: Contains list of arguments parsed from docopt (list)
        """

        super().__init__(arguments)
        self._username = self._arguments["<username>"]

    def run(self):
        """
        Run method for account delegate command.
        The user is prompted for the secret passphrase (input is masked).
        Then the user must confirm the transaction. If the user aborts the transaction then "Aborted." is printed and
        the transaction isn't sent.
        Otherwise the transaction is constructed using bpl_lib.transactions.Delegate and sent using bpl_api.
        If the transaction is successful then "Transaction sent successfully with id x" is displayed, otherwise
        "Failed to sent transaction: x" is displayed.

        :return: (None)
        """

        bpl_transactions = Client(NetworkConfig.get_peer()).api("transactions")
        NetworkInterface.use(NetworkConfig.get_config_identifier())

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
