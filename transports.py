import paramiko
import socket
import json

from config import SSH_CONFIG_FILE


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
            with open(SSH_CONFIG_FILE, 'r') as f:
                env = json.load(f)
            if not host:
                host = env.get("host")

            transports_ = env.get("transports")
            if not transports_:
                raise TransportConnetionError("Incorrect format of %s (param transports not found)" % SSH_CONFIG_FILE)
            ssh_ = transports_.get("SSH")
            if not ssh_:
                raise TransportConnetionError("Incorrect format of %s (param SSH not found)" % SSH_CONFIG_FILE)

            if not port:
                port = ssh_.get("port")
            if not login:
                login = ssh_.get("login")
            if not password:
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


transport_classes = {
    "SSH": SSHTransport
}


def get_transport(transport_name, host=None, port=None, login=None, password=None):
    transport = transport_classes.get(transport_name)
    if not transport:
        raise UnknownTransport("Transport name %s not found" % transport_name)
    return transport(host, port, login, password)
