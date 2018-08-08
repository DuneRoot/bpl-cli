from ascii_table import Table
from bpl_api import Client
from bpl_lib.network import Network as NetworkInterface
from bpl_lib.time import Time

from bpl_client.commands.Command import Command
from bpl_client.helpers.Exceptions import BPLClientAccountsException
from bpl_client.network.NetworkConfig import NetworkConfig


class Transactions(Command):

    def __init__(self, arguments):
        super().__init__(arguments)
        self._address = self._arguments["<address>"]

    def run(self):
        bpl_transactions = Client(NetworkConfig.get_peer()).api("transactions")
        NetworkInterface.use(NetworkConfig.get_peer())

        response = bpl_transactions.all_transactions({
            "senderId": self._address,
            "recipientId": self._address,
            "orderBy": "timestamp:desc"
        })

        if not response["success"]:
            raise BPLClientAccountsException({
                "message": "Failed to fetch transactions.",
                "error": response["error"]
            })

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
        parsed_transactions = {k: [] for k in [
            "id", "timestamp", "senderId", "recipientId", "amount", "fee", "confirmations"
        ]}

        for transaction in transactions:
            for key in parsed_transactions.keys():
                parsed_transactions[key].append(str(transaction.get(key, "N/A")))

        return parsed_transactions
