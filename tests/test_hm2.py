import importlib
import pytest
import docker
import time
import os
import json

from config import DB_FILE, SSH_CONFIG_FILE, CONTROLS_FILE
from transports import get_transport
from peewee_models import Scandata
from main import run


@pytest.fixture(scope="session", autouse=True)
def execute_before_any_test():
    global container

    client = docker.from_env()
    images = client.images.build(path="tests/sshd", dockerfile='Dockerfile')
    container = client.containers.run(image=images[0], detach=True, ports={"22/tcp": 23022})
    client.containers.prune()
    time.sleep(5)

    if os.path.isfile(SSH_CONFIG_FILE):
        os.rename(SSH_CONFIG_FILE, "%s.dump" % SSH_CONFIG_FILE)

    if os.path.isfile(DB_FILE):
        os.rename(DB_FILE, "%s.dump" % DB_FILE)

    with open(SSH_CONFIG_FILE, 'w') as f:
        data = {"host": "localhost", "transports": {"SSH": {"password": "pwd", "login": "root", "port": 23022}}}
        json.dump(data, f)


def test_connect_without_any_data():
    with get_transport("SSH"):
        pass


def test_first_script_while_docker_running():
    scriptpack = importlib.import_module("scripts.000_test_file_exists")
    with get_transport("SSH") as transport:
        assert scriptpack.main() == 2
        transport.exec("touch testfile")
        assert scriptpack.main() == 1


def test_main_run_function_with_db():
    run()
    scans_counts = Scandata.select().count()
    assert scans_counts > 0


def test_rm_cont():
    container.stop()
    container.remove()


def test_first_script_while_docker_stopped():
    scriptpack = importlib.import_module("scripts.000_test_file_exists")
    assert scriptpack.main() == 3


def test_db_json_back_and_check():
    os.remove(SSH_CONFIG_FILE)
    if os.path.isfile("%s.dump" % SSH_CONFIG_FILE):
        os.rename("%s.dump" % SSH_CONFIG_FILE, SSH_CONFIG_FILE)
    os.remove(DB_FILE)
    if os.path.isfile("%s.dump" % DB_FILE):
        os.rename("%s.dump" % DB_FILE, DB_FILE)

    with open(SSH_CONFIG_FILE, 'r') as f:
        env = json.load(f)

    assert env.get("host")

    transports_ = env["transports"]
    ssh_ = transports_["SSH"]

    assert ssh_.get("port")
    assert ssh_.get("login")
    assert ssh_.get("password")


def test_controls_json():
    if os.path.isfile(CONTROLS_FILE):
        with open(CONTROLS_FILE, 'r') as f:
            contrs = json.load(f)

        checks = list(map(lambda x: len(x) == 2, contrs))
        assert all(checks)
