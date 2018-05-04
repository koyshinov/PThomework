import json
import config


def test_config():
    assert config.DB_FILE == "sqlite.db"
    assert config.TRANSPORTS_CONFIG_FILE == "env.json"
    assert config.CONTROLS_FILE == "controls.json"

    # Status codes
    assert config.STATUS_COMPLIANT == 1
    assert config.STATUS_NOT_COMPLIANT == 2
    assert config.STATUS_NOT_APPLICABLE == 3
    assert config.STATUS_ERROR == 4
    assert config.STATUS_EXCEPTION == 5

    # Color console
    assert config.C_OKGREEN == '\033[92m'
    assert config.C_WARNING == '\033[93m'
    assert config.C_FAIL == '\033[91m'
    assert config.C_END == '\033[0m'
    assert config.C_BOLD == '\033[1m'


def test_env_json_ssh():
    with open(config.TRANSPORTS_CONFIG_FILE, 'r') as f:
        env = json.load(f)

    assert env.get("host")

    transports_ = env["transports"]
    ssh_ = transports_["SSH"]

    assert ssh_.get("port")
    assert ssh_.get("login")
    assert ssh_.get("password")


def test_env_json_mysql():
    with open(config.TRANSPORTS_CONFIG_FILE, 'r') as f:
        env = json.load(f)

    assert env.get("host")

    transports_ = env["transports"]
    mysql_ = transports_["MySQL"]

    assert mysql_.get("port")
    assert mysql_.get("login")
    assert mysql_.get("password")
    assert mysql_.get("db")


def test_controls_json():
    with open(config.CONTROLS_FILE, 'r') as f:
        contrs = json.load(f)

    for i in contrs:
        assert i.isdigit()

        contr = contrs[i]

        assert contr.get("filename")
        assert contr.get("title")
        assert contr.get("requirements")
        assert contr.get("description")

