import pytest

from transports import get_transport, TransportError, UnknownTransport, TransportConnetionError


def test_except_transport_ssh_error_1():
    with get_transport("SSH", "localhost", 22022, "root", "pwd") as transport:
        with pytest.raises(TransportError, message="Expecting TransportError"):
            transport.exec()


def test_except_transport_ssh_error_2():
    with get_transport("SSH", "localhost", 22022, "root", "pwd") as transport:
        with pytest.raises(TransportError, message="Expecting TransportError"):
            transport.exec("")


def test_except_transport_ssh_error_3():
    with get_transport("SSH", "localhost", 22022, "root", "pwd") as transport:
        with pytest.raises(TransportError, message="Expecting TransportError"):
            transport.get_file()


def test_except_transport_ssh_error_4():
    with get_transport("SSH", "localhost", 22022, "root", "pwd") as transport:
        with pytest.raises(TransportError, message="Expecting TransportError"):
            transport.get_file("")


def test_except_unknown_transport_ssh():
    with pytest.raises(UnknownTransport, message="Expecting UnknownTransport"):
        with get_transport("SFTP", "localhost", 22022, "root", "pwd"):
            pass


def test_wrong_data_port_ssh():
    with pytest.raises(TransportConnetionError, message="Expecting TransportConnetionError"):
        with get_transport("SSH", "localhost", 22023, "root", "pwd"):
            pass


def test_wrong_data_login_passw_ssh():
    with pytest.raises(TransportConnetionError, message="Expecting TransportConnetionError"):
        with get_transport("SSH", "localhost", 22022, "roo", "pwd"):
            pass

    with pytest.raises(TransportConnetionError, message="Expecting TransportConnetionError"):
        with get_transport("SSH", "localhost", 22022, "root", "pwd1"):
            pass


def test_wrong_data_host_ssh():
    with pytest.raises(TransportConnetionError, message="Expecting TransportConnetionError"):
        with get_transport("SSH", "8.8.8.8", 22022, "root", "pwd"):
            pass
