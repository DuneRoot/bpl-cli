class BPLClientNetworkException(Exception):

    def __str__(self):
        return "[ERROR] Error: BPLClientNetworkError, Response: {0}".format(super().__str__())


class BPLClientAccountsException(Exception):

    def __str__(self):
        return "[ERROR] Error: BPLClientAccountsError, Response: {0}".format(super().__str__())
