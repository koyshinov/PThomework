import importlib
import pytest
import docker
import time
import os
import json

from transports import get_transport
from peewee_models import Scandata
from main import run


@pytest.fixture(scope="session", autouse=True)
def execute_before_any_test():
    global container

    client = docker.from_env()
    images = client.images.build(path="test/sshd", dockerfile='Dockerfile')
    container = client.containers.run(image=images[0], detach=True, ports={"22/tcp": 23022})
    client.containers.prune()
    time.sleep(5)

    if os.path.isfile("env.json"):
        os.rename("env.json", "env.json.dump")

    if os.path.isfile("sqlite.db"):
        os.rename("sqlite.db", "sqlite.db.dump")

    with open('env.json', 'w') as f:
        data = {"host": "localhost", "transports": {"SSH": {"password": "pwd", "login": "root", "port": 23022}}}
        json.dump(data, f)


def test_connect_without_any_data():
    transport = get_transport("SSH")
    del(transport)


def test_first_script_while_docker_running():
    scriptpack = importlib.import_module("scripts.000_test_file_exists")
    transport = get_transport("SSH")
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
    os.remove("env.json")
    if os.path.isfile("env.json.dump"):
        os.rename("env.json.dump", "env.json")
    os.remove("sqlite.db")
    if os.path.isfile("sqlite.db.dump"):
        os.rename("sqlite.db.dump", "sqlite.db")

    with open('env.json', 'r') as f:
        env = json.load(f)

    host = env["host"]

    transports_ = env["transports"]
    ssh_ = transports_["SSH"]

    port = ssh_["port"]
    login = ssh_["login"]
    password = ssh_["password"]


def test_controls_json():
    with open("controls.json", 'r') as f:
        contrs = json.load(f)

    checks = list(map(lambda x: len(x) == 2, contrs))
    assert all(checks)