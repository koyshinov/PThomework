from transports import get_transport


def test_connect_with_data():
    with get_transport("MySQL", "localhost", 43306, "root", "pwd123", "sadb"):
        pass


def test_connect_without_data():
    with get_transport("MySQL"):
        pass
