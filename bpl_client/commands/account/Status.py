from ascii_table import Table
from bpl_api import Client

from bpl_client.commands.Command import Command
from bpl_client.helpers.Exceptions import BPLClientAccountsException
from bpl_client.helpers.Util import SortedDictionary
from bpl_client.network.NetworkConfig import NetworkConfig


class Status(Command):

    def __init__(self, arguments):
        super().__init__(arguments)
        self._bpl_accounts = Client(NetworkConfig.get_peer()).api("accounts")
        self._address = self._arguments["<address>"]

    def run(self):
        self._get_account()
        self._get_delegate()

    def _get_account(self):
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
        print(Table([account.headers(), account.values()]))

    def _get_delegate(self):
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

            print("\nDelegate ({0})".format(delegate["username"]))
            print(Table([delegate.headers(), delegate.values()]))
