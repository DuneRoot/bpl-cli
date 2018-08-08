from ascii_table import Table
from bpl_api import Client

from bpl_client.helpers.Exceptions import BPLClientAccountsException
from bpl_client.network.NetworkConfig import NetworkConfig
from bpl_client.helpers.Util import SortedDictionary
from bpl_client.commands.Command import Command


class Status(Command):

    def __init__(self, arguments):
        """
        Account status command constructor
        Initializes _bpl_accounts and _address

        :param arguments: Contains list of arguments parsed from docopt (list)
        """

        super().__init__(arguments)
        self._bpl_accounts = Client(NetworkConfig.get_peer()).api("accounts")
        self._address = self._arguments["<address>"]

    def run(self):
        """
        Run method for account status command
        Displays the status of the specified account and any delegates the account voted for.

        :return: (None)
        """

        self._get_account()
        self._get_delegate()

    def _get_account(self):
        """
        Used to fetch the status of the account and then display it using a ascii_table.Table object

        :return: (None)
        """

        account = self._bpl_accounts.account(self._address)

        if not account["success"]:
            raise BPLClientAccountsException({
                "message": "Address unknown on the blockchain.",
                "address": self._address
            })

        account = SortedDictionary({
            str(k): str(v) for k, v in account["account"].items()
            if v and len(str(v)) > 0
        })
        del account["address"]

        print("\nAddress Summary")
        print(Table([account.names(), account.values()]))

    def _get_delegate(self):
        """
        Used to fetch the status of any delegates the account voted for and display them individually using a
        ascii_table.Table object

        :return: (None)
        """

        votes = self._bpl_accounts.votes(self._address)

        if not votes["success"]:
            raise BPLClientAccountsException({
                "message": "Delegate unknown on the blockchain.",
                "error": votes["error"]
            })

        for vote in votes["delegates"]:
            delegate = SortedDictionary(vote)
            del delegate["address"]
            del delegate["publicKey"]

            print("\nVoted Delegate ({0})".format(delegate["username"]))
            print(Table([delegate.names(), delegate.values()]))
