from bpl_lib.crypto import Signature, sha256

from bpl_client.commands.Command import Command


class Verify(Command):

    def __init__(self, arguments):
        """
        Message verify command constructor
        Initializes _message and _public_key.

        :param arguments: Contains list of arguments parsed from docopt (list)
        """

        super().__init__(arguments)
        self._message = sha256(self._arguments["<message>"].encode())
        self._public_key = self._arguments["<publicKey>"]

    def run(self):
        """
        Run method for message verify command.
        Prints prompt for the user to enter message signature.
        Uses bpl_lib.crypto.Signature to verify message.
        Then displays the result "Signature is valid" or "Signature is invalid" based on result from Signature.verify.

        :return: (None)
        """

        signature = input("Enter signature: ")

        valid = Signature.verify(self._public_key, self._message, signature)
        print("\nSuccessfully verified signed message.")
        if valid:
            print("Signature is valid.")
        else:
            print("Signature is invalid.")
