import json
import sys

from bpl_client.helpers.Exceptions import BPLClientNetworkException
from bpl_client.helpers.Constants import NETWORK_CONFIG, NETWORK_CONFIGS
from bpl_client.helpers.Util import read_file


class NetworkConfig:

    @staticmethod
    def get_configs():
        """
        Fetches all configs stored in configs.json

        :return: (dict)
        """

        return json.loads(read_file(NETWORK_CONFIGS))

    @staticmethod
    def get_config():
        """
        Fetches current config

        :return: (dict)
        """

        return NetworkConfig.get_configs()[NetworkConfig.get_config_identifier()]

    @staticmethod
    def get_config_identifiers():
        """
        Fetches list of config identifiers stored in configs.json

        :return: (list)
        """

        return json.loads(read_file(NETWORK_CONFIGS)).keys()

    @staticmethod
    def get_peer():
        """
        Fetches the peer address stored in config.json.

        :return: address of peer (string)
        """

        return NetworkConfig.get_config()["peer address"]

    @staticmethod
    def validate_identifier(config_identifier):
        """
        Returns True if :param config_identifier is a member of the stored config identifiers set

        :param config_identifier: (string)
        :return: (boolean)
        """

        return config_identifier in NetworkConfig.get_config_identifiers()

    @staticmethod
    def get_config_identifier():
        """
        Reads and parses config identifier stored in config.json. If no data is stored in config.json then a
        BPLClientNetworkException is raised.

        :return: config identifier (string)
        """

        try:
            config_identifier = json.loads(read_file(NETWORK_CONFIG))["identifier"]
        except PermissionError:
            print(BPLClientNetworkException({
                "message": "client has insufficient permissions to read config.json. "
                         + "Please configure read access of config.json"
            }), file=sys.stderr)
            sys.exit(13)
        except:
            print(BPLClientNetworkException({"message": (
                "network config not setup. Please use bpl-cli network config new or bpl-cli network config use."
            )}), file=sys.stderr)
            sys.exit(1)

        if not NetworkConfig.validate_identifier(config_identifier):
            print(BPLClientNetworkException({
                "message": "invalid config identifier",
                "config identifiers": NetworkConfig.get_config_identifiers(),
                "config identifier": config_identifier
            }), file=sys.stderr)
            sys.exit(1)

        return config_identifier
