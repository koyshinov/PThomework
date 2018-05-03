import json

from config import TRANSPORTS_CONFIG_FILE, CONTROLS_FILE


def test_env_json_ssh():
    with open(TRANSPORTS_CONFIG_FILE, 'r') as f:
        env = json.load(f)

    assert env.get("host")

    transports_ = env["transports"]
    ssh_ = transports_["SSH"]

    assert ssh_.get("port")
    assert ssh_.get("login")
    assert ssh_.get("password")


def test_env_json_mysql():
    with open(TRANSPORTS_CONFIG_FILE, 'r') as f:
        env = json.load(f)

    assert env.get("host")

    transports_ = env["transports"]
    mysql_ = transports_["MySQL"]

    assert mysql_.get("port")
    assert mysql_.get("login")
    assert mysql_.get("password")
    assert mysql_.get("db")


def test_controls_json():
    with open(CONTROLS_FILE, 'r') as f:
        contrs = json.load(f)

    for i in contrs:
        assert i.isdigit()

        contr = contrs[i]

        assert contr.get("filename")
        assert contr.get("title")
        assert contr.get("requirements")
        assert contr.get("description")

