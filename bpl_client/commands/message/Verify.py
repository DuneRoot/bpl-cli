from bpl_lib.crypto import Signature, sha256

from bpl_client.commands.Command import Command


class Verify(Command):

    def __init__(self, arguments):
        super().__init__(arguments)
        self._message = sha256(self._arguments["<message>"].encode())
        self._public_key = self._arguments["<publicKey>"]

    def run(self):
        signature = input("Enter signature: ")

        valid = Signature.verify(self._public_key, self._message, signature)
        print("\nSuccessfully verified signed message.")
        if valid:
            print("Signature is valid.")
        else:
            print("Signature is invalid.")
