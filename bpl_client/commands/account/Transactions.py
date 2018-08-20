import sys

from bpl_lib.network import Network as NetworkInterface
from ascii_table import Table
from bpl_lib.time import Time
from bpl_api import Client

from bpl_client.helpers.Exceptions import BPLClientAccountsException
from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.commands.Command import Command


class Transactions(Command):

    def __init__(self, arguments):
        """
        Account transactions command constructor
        Initializes _address

        :param arguments: contains list of arguments parsed from docopt (list)
        """

        super().__init__(arguments)
        self._address = self._arguments["<address>"]

    def run(self):
        """
        Run method for account transactions command.
        Requests transactions of an address using bpl_api.
        If response from request is successful then displays transactions using a ascii_table.Table object.
        If response from request is unsuccessful then a BPLClientAccountsException is raised.

        :return: (None)
        """

        bpl_transactions = Client(NetworkConfig.get_peer()).api("transactions")
        NetworkInterface.use(NetworkConfig.get_config_identifier())

        response = bpl_transactions.all_transactions({
            "senderId": self._address,
            "recipientId": self._address,
            "orderBy": "timestamp:desc"
        })

        if not response["success"]:
            print(BPLClientAccountsException({
                "message": "Failed to fetch transactions.",
                "error": response["error"]
            }), file=sys.stderr)
            sys.exit(1)

        transactions = self._parse_transactions(response["transactions"])

        print("\nTransactions (Address: {0})".format(self._address))
        print(Table([
            {
                "Header": "Transaction ID",
                "Contents": transactions["id"]
            },
            {
                "Header": "Timestamp",
                "Contents": list(map(lambda x: Time.get_real_time(int(x)), transactions["timestamp"]))
            },
            {
                "Header": "Sender",
                "Contents": transactions["senderId"]
            },
            {
                "Header": "Recipient",
                "Contents": transactions["recipientId"]
            },
            {
                "Header": "Amount",
                "Contents": transactions["amount"]
            },
            {
                "Header": "Fee",
                "Contents": transactions["fee"]
            },
            {
                "Header": "Confirmations",
                "Contents": transactions["confirmations"]
            }
        ]))

    def _parse_transactions(self, transactions):
        """
        Returns transactions in a format of
        {id:[...], timestamp:[...], senderId:[...], recipientId:[...], amount:[...], fee:[...], confirmations:[...]}.
        This format is more beneficial for ascii_table.Table

        :param transactions: list of transactions from response (list)
        :return: (dict)
        """

        parsed_transactions = {k: [] for k in [
            "id", "timestamp", "senderId", "recipientId", "amount", "fee", "confirmations"
        ]}

        for transaction in transactions:
            for key in parsed_transactions.keys():
                parsed_transactions[key].append(str(transaction.get(key, "N/A")))

        return parsed_transactions
