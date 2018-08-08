"""
BPL Client

Usage:
  bpl-cli network config setup
  bpl-cli network config show
  bpl-cli network peers
  bpl-cli network status
  bpl-cli account status <address>
  bpl-cli account transactions <address>
  bpl-cli account send <amount> <recipient>
  bpl-cli account vote <username>
  bpl-cli account delegate <username>
  bpl-cli message sign <message>
  bpl-cli message verify <message> <publicKey>

Options:
  -h --help                 Show this screen.
  --version                 Show version.

Help:
  For help using this client, please see ...
"""

from importlib import import_module
from functools import reduce
from docopt import docopt
import json

from bpl_client.helpers.Constants import COMMANDS_JSON
from bpl_client.helpers.Util import read_file


class Client:

    def __init__(self, version=0):
        self._options = docopt(__doc__, version=version)
        self._arguments = {
            k: v for k, v in self._options.items()
            if not isinstance(v, bool)
        }

        commands_json = json.loads(read_file(COMMANDS_JSON))
        command = list(filter(lambda x: self._is_command(x["Conditions"]), commands_json))[0]

        getattr(
            import_module("bpl_client.commands.{0}".format(command["Module Identifier"])),
            command["Class Identifier"]
        )(self._arguments).run()

    def _is_command(self, conditions):
        return reduce(lambda x, y: x and y, map(lambda y: self._options[y], conditions))
