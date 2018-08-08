class Command:

    def __init__(self, arguments):
        """
        Constructor for command parent class

        :param arguments: Contains list of arguments parsed from docopt (list)
        """

        self._arguments = arguments

    def run(self):
        raise NotImplementedError
