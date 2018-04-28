import paramiko
import socket
import json


class TransportError(Exception):
    pass


class TransportConnetionError(Exception):
    pass


class TransportCommandError(Exception):
    pass


class UnknownTransport(Exception):
    pass


class SSHTransport:
    def __init__(self, host, port, login, password):
        if not all([host, port, login, password]):
            with open('env.json', 'r') as f:
                env = json.load(f)
            if not host:
                host = env.get("host")

            transports_ = env.get("transports")
            if not transports_:
                raise TransportConnetionError()
            ssh_ = transports_.get("SSH")
            if not ssh_:
                raise TransportConnetionError

            if not port:
                port = ssh_.get("port")
            if not login:
                login = ssh_.get("login")
            if not password:
                password = ssh_.get("password")

            if not all([host, port, login, password]):
                raise TransportConnetionError

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=host, username=login, password=password, port=port, timeout=5)
        except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.ssh_exception.AuthenticationException,
                paramiko.ssh_exception.SSHException, socket.timeout):
            raise TransportConnetionError()

    def exec(self, command=None):
        if not command:
            raise TransportError()
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
        except paramiko.ssh_exception.SSHException:
            raise TransportError()

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


transport_classes = {
    "SSH": SSHTransport
}


def get_transport(transport_name, host=None, port=None, login=None, password=None):
    transport = transport_classes.get(transport_name)
    if not transport:
        raise UnknownTransport()
    return transport(host, port, login, password)
