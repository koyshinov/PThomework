import paramiko
import socket
import json

import pymysql.cursors
from contextlib import contextmanager

from config import TRANSPORTS_CONFIG_FILE


class TransportError(Exception):
    pass


class TransportConnetionError(Exception):
    pass


class TransportCommandError(Exception):
    pass


class UnknownTransport(Exception):
    pass


class SSHTransport:
    def __init__(self, *args):
        if len(args) == 4:
            host, port, login, password = args
        else:
            with open(TRANSPORTS_CONFIG_FILE, 'r') as f:
                env = json.load(f)

            host = env.get("host")
            transports_ = env.get("transports")

            if not transports_:
                raise TransportConnetionError("Incorrect format of %s (param transports not found)" %
                                              TRANSPORTS_CONFIG_FILE)
            ssh_ = transports_.get("SSH")
            if not ssh_:
                raise TransportConnetionError("Incorrect format of %s (param SSH not found)" % TRANSPORTS_CONFIG_FILE)

            port = ssh_.get("port")
            login = ssh_.get("login")
            password = ssh_.get("password")

            if not all([host, port, login, password]):
                raise TransportConnetionError("Some of params (host, port, login, password) not found")

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=host, username=login, password=password, port=port, timeout=5)
        except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.ssh_exception.AuthenticationException,
                paramiko.ssh_exception.SSHException, socket.timeout):
            raise TransportConnetionError("Error of ssh connection")

    def exec(self, command=None):
        if not command:
            raise TransportError("Command not found")

        stdin, stdout, stderr = self.client.exec_command(command)

        error = stderr.read()

        if error:
            raise TransportCommandError(error.decode("utf-8"))

        return stdout.read().decode("utf-8")

    def get_file(self, path=None):
        if not path:
            raise TransportError()
        sftp_client = self.client.open_sftp()
        stdout = sftp_client.file(path, mode="r").read()
        return stdout.decode("utf-8")

    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()


class MySQLTransport:
    def __init__(self, *args):
        if len(args) == 5:
            host, port, login, password, dbname = args
        else:
            with open(TRANSPORTS_CONFIG_FILE, 'r') as f:
                env = json.load(f)

            host = env.get("host")
            transports_ = env.get("transports")

            if not transports_:
                raise TransportConnetionError("Incorrect format of %s (param transports not found)" %
                                              TRANSPORTS_CONFIG_FILE)
            mysql_ = transports_.get("MySQL")
            if not mysql_:
                raise TransportConnetionError("Incorrect format of %s (param MySQL not found)" % TRANSPORTS_CONFIG_FILE)

            port = mysql_.get("port")
            login = mysql_.get("login")
            password = mysql_.get("password")
            dbname = mysql_.get("db")

            if not all([host, port, login, password, dbname]):
                raise TransportConnetionError("Some of params (host, port, login, password, db) not found")

        try:
            self.connection = pymysql.connect(host=host, user=login, port=port, password=password, db=dbname,
                                              charset='utf8', cursorclass=pymysql.cursors.DictCursor, unix_socket=False)
        except (pymysql.err.OperationalError, ):
            raise TransportConnetionError("Error of mysql connection")

    def sqlexec(self, sql=None, params=None):
        if not sql:
            raise TransportError("SQL command not found")

        with self.connection.cursor() as cursor:
            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
            except (pymysql.err.InternalError, pymysql.err.ProgrammingError, TypeError) as e:
                raise TransportCommandError(e)

            self.connection.commit()
            return cursor.fetchone()

    def __del__(self):
        if hasattr(self, "connection"):
            self.connection.close()


transport_classes = {
    "SSH": SSHTransport,
    "MySQL": MySQLTransport
}


@contextmanager
def get_transport(transport_name, *args):
    transport = transport_classes.get(transport_name)

    if not transport:
        raise UnknownTransport("Transport name %s not found" % transport_name)
    yield transport(*args)

    del(transport)
