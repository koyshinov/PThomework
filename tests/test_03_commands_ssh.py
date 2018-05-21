from transports import get_transport


def test_passwd_file():
    with get_transport("SSH") as transport:
        passwd_file1 = transport.get_file("/etc/passwd")
        passwd_file2 = transport.exec("cat /etc/passwd")

        assert passwd_file1 == passwd_file2


def test_double_cmnd():
    with get_transport("SSH") as transport:
        text = "Some interesting data"
        result = transport.exec("echo \"%s\" > somefile; cat somefile" % text)
        transport.exec("rm somefile")

        assert "%s\n" % text == result
