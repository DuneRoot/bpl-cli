import sys


def read_file(file_location):
    """
    Reads the file stored at :param file_location

    :param file_location: absolute path for the file to be read (string)
    :return: contents of file (string)
    """

    try:
        with open(file_location, "r") as file:
            return file.read()
    except FileNotFoundError:
        print("[ERROR] Error: FileNotFoundError, Response: Failed to read {0}".format(file_location), file=sys.stderr)
        return ""


def write_file(file_location, data):
    """
    Writes :param data to the file stored at :param file_locations

    :param file_location: absolute path for the file that is being written too (string)
    :param data: data that will be written to the file (string)
    :return: (None)
    """

    try:
        with open(file_location, "w") as file:
            file.write(data)
    except PermissionError:
        print(
            "[ERROR] Error: PermissionError, Response: Failed to write to "
          + "{0}. Please configure write access for {0}".format(file_location), file=sys.stderr
        )
        sys.exit(13)


class SortedDictionary:
    """
    SortedDictionary Class

    Class that sorts a dictionary based on the length of the value data item
    """

    def __init__(self, dictionary):
        """
        SortedDictionary Constructor

        :param dictionary: dictionary to be sorted. In format {key:value}, where key is string
                           and value is data item(dict)
        """

        self._dictionary = self._sort_dictionary(dictionary)

    def _sort_dictionary(self, dictionary):
        """
        Private method that sorts the dictionary

        :param dictionary: dictionary to be sorted
        :return: Sorted dictionary (list of tuples)
        """

        return sorted(dictionary.items(), key=lambda x: len(str(x[1])))

    def names(self):
        """
        Returns names for an ascii-table Table object

        :return: (dict)
        """

        return {
            "Header": "Name",
            "Contents": map(lambda x: str(x[0]), self._dictionary)
        }

    def values(self):
        """
        Returns values for an ascii-table Table object

        :return: (dict)
        """

        return {
            "Header": "Value",
            "Contents": map(lambda x: str(x[1]), self._dictionary)
        }

    def __getitem__(self, key):
        """
        Returns a value from a (key, value) pair in the SortedDictionary object. Uses simple linear search algorithm.

        :param key: key of (key, value) pair in dictionary (string)
        :return: value of (key, value) pair
        """

        value = list(filter(lambda x: key == x[0], self._dictionary))
        if not len(value):
            return ""

        return value[0][1]

    def __delitem__(self, key):
        """
        Removes a key, value pair from the SortedDictionary object.

        :param key: key of (key, value) pair in dictionary
        :return: (None)
        """

        self._dictionary = list(filter(lambda x: x[0] != key, self._dictionary))

    def __len__(self):
        """
        Returns the length of the SortedDictionary object

        :return: length (integer)
        """

        return len(self._dictionary)

    def __repr__(self):
        """
        Returns string representation of the SortedDictionary object

        :return: string representation of the SortedDictionary object (string)
        """

        return str(self._dictionary)
