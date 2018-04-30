import pytest
import docker
import time

from transports import get_transport, TransportError, UnknownTransport, TransportConnetionError


@pytest.fixture(scope="session", autouse=True)
def execute_before_any_test():
    global container

    client = docker.from_env()
    images = client.images.build(path="tests/sshd", dockerfile='Dockerfile')
    container = client.containers.run(image=images[0], detach=True, ports={"22/tcp": 23022})
    client.containers.prune()
    time.sleep(5)


def test_connect_with_data():
    transport = get_transport("SSH", "localhost", 23022, "root", "pwd")
    del(transport)


def test_passwd_file():
    transport = get_transport("SSH", "localhost", 23022, "root", "pwd")
    passwd_file1 = transport.get_file("/etc/passwd")
    passwd_file2 = transport.exec("cat /etc/passwd")

    assert len(passwd_file1) > 10
    assert isinstance(passwd_file1, str)
    assert "root:x:0:0:root:/root:/bin/bash" in passwd_file1
    assert passwd_file1 == passwd_file2

    del(transport)


def test_except_transport_error_1():
    """
    with pytest.raises(ZeroDivisionError, message="Expecting ZeroDivisionError"):
        pass
    """
    transport = get_transport("SSH", "localhost", 23022, "root", "pwd")

    with pytest.raises(TransportError, message="Expecting TransportError"):
        transport.exec()

    del(transport)


def test_except_transport_error_2():
    transport = get_transport("SSH", "localhost", 23022, "root", "pwd")

    with pytest.raises(TransportError, message="Expecting TransportError"):
        transport.exec("")

    del(transport)


def test_except_transport_error_3():
    transport = get_transport("SSH", "localhost", 23022, "root", "pwd")

    with pytest.raises(TransportError, message="Expecting TransportError"):
        transport.get_file()

    del(transport)


def test_except_transport_error_4():
    transport = get_transport("SSH", "localhost", 23022, "root", "pwd")

    with pytest.raises(TransportError, message="Expecting TransportError"):
        transport.get_file("")

    del(transport)


def test_except_unknown_transport():
    with pytest.raises(UnknownTransport, message="Expecting UnknownTransport"):
        transport = get_transport("SFTP", "localhost", 23022, "root", "pwd")
        del(transport)


def test_wrong_data_port():
    with pytest.raises(TransportConnetionError, message="Expecting TransportConnetionError"):
        transport = get_transport("SSH", "localhost", 23023, "root", "pwd")
        del(transport)


def test_wrong_data_login_passw():
    with pytest.raises(TransportConnetionError, message="Expecting TransportConnetionError"):
        transport = get_transport("SSH", "localhost", 23022, "roo", "pwd")
        del (transport)

    with pytest.raises(TransportConnetionError, message="Expecting TransportConnetionError"):
        transport = get_transport("SSH", "localhost", 23022, "root", "pwd1")
        del (transport)


def test_wrong_data_host():
    with pytest.raises(TransportConnetionError, message="Expecting TransportConnetionError"):
        transport = get_transport("SSH", "8.8.8.8", 23022, "root", "pwd")
        del(transport)


def test_rm_cont():
    container.stop()
    container.remove()
