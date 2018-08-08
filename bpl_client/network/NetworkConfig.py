import json

from bpl_client.helpers.Exceptions import BPLClientNetworkException
from bpl_client.helpers.Constants import NETWORK_CONFIG
from bpl_client.helpers.Util import read_file


class NetworkConfig:

    @staticmethod
    def get_config():
        try:
            config = json.loads(read_file(NETWORK_CONFIG))
        except:
            raise BPLClientNetworkException({
                "message": "network config not setup. Please use bpl-cli network config setup."
            })

        return config

    @staticmethod
    def get_peer():
        return NetworkConfig.get_config()["peer address"]
