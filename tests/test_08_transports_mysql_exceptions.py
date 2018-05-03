import pytest

from transports import get_transport, TransportError, TransportConnetionError, TransportCommandError


SQL_INSERT = "INSERT INTO `users` (`email`, `password`) VALUES (\"some\", \"some\");"


def test_except_transport_error_1():
    with get_transport("MySQL", "localhost", 43306, "root", "pwd123", "sadb") as transport:
        with pytest.raises(TransportError, message="Expecting TransportError"):
            transport.sqlexec()


def test_wrong_data_port():
    with pytest.raises(TransportConnetionError, message="Expecting TransportConnetionError"):
        with get_transport("MySQL", "localhost", 43307, "root", "pwd123", "sadb"):
            pass


def test_wrong_data_login_passw():
    with pytest.raises(TransportConnetionError, message="Expecting TransportConnetionError"):
        with get_transport("MySQL", "localhost", 43306, "root123", "pwd123", "sadb"):
            pass

    with pytest.raises(TransportConnetionError, message="Expecting TransportConnetionError"):
        with get_transport("MySQL", "localhost", 43306, "root", "pwd123456", "sadb"):
            pass


def test_wrong_data_host():
    with pytest.raises(TransportConnetionError, message="Expecting TransportConnetionError"):
        with get_transport("MySQL", "8.8.8.8", 43306, "root", "pwd123", "sadb"):
            pass


def test_wrong_data_db():
    with pytest.raises(TransportConnetionError, message="Expecting TransportConnetionError"):
        with get_transport("MySQL", "localhost", 43307, "root", "pwd123", "sadbdbdb"):
            pass


def test_invalid_sql1():
    with pytest.raises(TransportCommandError, message="Expecting TransportCommandError"):
        with get_transport("MySQL", "localhost", 43306, "root", "pwd123", "sadb") as transport:
            transport.sqlexec("SELECT SELECT")


def test_invalid_sql2():
    with pytest.raises(TransportCommandError, message="Expecting TransportCommandError"):
        with get_transport("MySQL", "localhost", 43306, "root", "pwd123", "sadb") as transport:
            transport.sqlexec(SQL_INSERT)


def test_invalid_sql3():
    with pytest.raises(TransportCommandError, message="Expecting TransportCommandError"):
        with get_transport("MySQL", "localhost", 43306, "root", "pwd123", "sadb") as transport:
            transport.sqlexec("SELECT %s", ("1", "blabla"))


def test_invalid_sql4():
    with pytest.raises(TransportCommandError, message="Expecting TransportCommandError"):
        with get_transport("MySQL", "localhost", 43306, "root", "pwd123", "sadb") as transport:
            transport.sqlexec("SELECT %s")