class Command:

    def __init__(self, arguments):
        """
        Command Constructor

        :param arguments: Contains list of arguments parsed from docopt (list)
        """

        self._arguments = arguments

    def run(self):
        """
        Abstract method run for command

        :return: (None)
        """

        raise NotImplementedError
