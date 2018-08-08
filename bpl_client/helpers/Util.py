import sys


def read_file(file_location):
    try:
        with open(file_location, "r") as file:
            return file.read()
    except FileNotFoundError:
        print("Failed to read {0}", file=sys.stderr)
        return ""


def write_file(file_location, data):
    with open(file_location, "w") as file:
        file.write(data)


class SortedDictionary:

    def __init__(self, dictionary):
        self._dictionary = self._sort_dictionary(dictionary)

    def _sort_dictionary(self, dictionary):
        return sorted(dictionary.items(), key=lambda x: len(str(x[1])))

    def headers(self):
        return {
            "Header": "Name",
            "Contents": map(lambda x: str(x[0]), self._dictionary)
        }

    def values(self):
        return {
            "Header": "Value",
            "Contents": map(lambda x: str(x[1]), self._dictionary)
        }

    def __getitem__(self, item):
        for k, v in self._dictionary:
            if item == k:
                return v
        return ""

    def __delitem__(self, key):
        self._dictionary = list(filter(lambda x: x[0] != key, self._dictionary))

    def __len__(self):
        return len(self._dictionary)

    def __repr__(self):
        return str(self._dictionary)
