import json

from bpl_client.helpers.Exceptions import BPLClientNetworkException
from bpl_client.helpers.Constants import NETWORK_CONFIG
from bpl_client.helpers.Util import read_file


class NetworkConfig:

    @staticmethod
    def get_config():
        """
        Reads and parses data stored in config.json. If no data is stored in config.json then a
        BPLClientNetworkException is raised.

        :return: config.json (dict)
        """

        try:
            config = json.loads(read_file(NETWORK_CONFIG))
        except:
            raise BPLClientNetworkException({
                "message": "network config not setup. Please use bpl-cli network config setup."
            })

        return config

    @staticmethod
    def get_peer():
        """
        Fetches the peer address stored in config.json.

        :return: address of peer (string)
        """

        return NetworkConfig.get_config()["peer address"]
