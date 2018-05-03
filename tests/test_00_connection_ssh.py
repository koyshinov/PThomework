from transports import get_transport


def test_connect_with_data():
    with get_transport("SSH", "localhost", 22022, "root", "pwd"):
        pass


def test_connect_without_data():
    with get_transport("SSH"):
        pass
