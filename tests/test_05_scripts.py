import importlib
import json
import os

from config import TRANSPORTS_CONFIG_FILE
from transports import get_transport


def test_first_script_while_ssh_conected():
    scriptpack = importlib.import_module("scripts.000_test_file_exists")
    with get_transport("SSH") as transport:
        assert scriptpack.main() == 2

        transport.exec("touch testfile")
        result = scriptpack.main()

        transport.exec("rm testfile")

        assert result == 1


def test_first_script_while_ssh_without_connection():
    if os.path.isfile(TRANSPORTS_CONFIG_FILE):
        os.rename(TRANSPORTS_CONFIG_FILE, "%s.dump" % TRANSPORTS_CONFIG_FILE)

    with open(TRANSPORTS_CONFIG_FILE, 'w') as f:
        data = {"host": "localhost", "transports": {"SSH": {"password": "pwd", "login": "root123", "port": 22023}}}
        json.dump(data, f)

    result = importlib.import_module("scripts.000_test_file_exists").main()

    if os.path.isfile("%s.dump" % TRANSPORTS_CONFIG_FILE):
        os.rename("%s.dump" % TRANSPORTS_CONFIG_FILE, TRANSPORTS_CONFIG_FILE)

    assert result == 3
