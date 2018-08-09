from getpass import getpass

from bpl_lib.transactions import Vote as VoteTransaction
from bpl_lib.network import Network as NetworkInterface
from bpl_api import Client

from bpl_client.helpers.Exceptions import BPLClientAccountsException
from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.commands.Command import Command


class Vote(Command):

    def __init__(self, arguments):
        """
        Account vote command constructor
        Initializes _username

        :param arguments: contains list of arguments parsed from docopt (list)
        """

        super().__init__(arguments)
        self._username = self._arguments["<username>"]

    def run(self):
        """
        Run method for account vote command.
        Verifies that self._username is the name of a valid delegate.
        If self._username is invalid then a BPLClientAccountsException is raised.
        Otherwise the user is prompted for the secret passphrase (input is masked).
        Then the user must confirm the transaction. If the user aborts the transaction then "Aborted." is printed and
        the transaction isn't sent.
        Otherwise the transaction is constructed using bpl_lib.transactions.Vote and sent using bpl_api.
        If the transaction is successful then "Transaction sent successfully with id x" is displayed, otherwise
        "Failed to sent transaction: x" is displayed.

        :return: (None)
        """

        bpl_transactions = Client(NetworkConfig.get_peer()).api("transactions")
        NetworkInterface.use(NetworkConfig.get_config_identifier())

        if not self._verify_delegate():
            raise BPLClientAccountsException({
                "message": "Invalid delegate.",
                "delegate": self._username
            })

        votes = ["+" + self._get_public_key()]
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
        """
        Used to verify whether self._username stores the name of a valid delegate

        :return: (boolean)
        """

        return Client(NetworkConfig.get_peer()).api("delegates").delegate(self._username)["success"]

    def _get_public_key(self):
        """
        Used to return the public key of the delegate

        :return: (string)
        """

        return Client(NetworkConfig.get_peer()).api("delegates").delegate(self._username)["delegate"]["publicKey"]
