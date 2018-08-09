import os

from bpl_client import ROOT

COMMANDS_JSON = os.path.join(ROOT, "commands.json")
NETWORK_CONFIG = os.path.join(ROOT, "network\\config.json")
NETWORK_CONFIGS = os.path.join(ROOT, "network\\configs.json")

PEER_ADDRESS_REGEX = r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$"
VERSION_REGEX = r"^(\d{1,3})$"
EPOCH_REGEX = r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})$"

BPL = 100000000
