from config import STATUS_NOT_APPLICABLE, STATUS_COMPLIANT, STATUS_NOT_COMPLIANT, STATUS_ERROR
from transports import get_transport, TransportConnetionError


def main():
    cmnd = 'if [ -f "%s" ]; then echo "Exist"; fi'
    filename = "testfile"

    try:
        with get_transport("SSH") as transport:
            result = transport.exec(cmnd % filename)

    except TransportConnetionError:
        return STATUS_NOT_APPLICABLE

    if "Exist" in result:
        return STATUS_COMPLIANT
    elif result == "":
        return STATUS_NOT_COMPLIANT
    else:
        return STATUS_ERROR
