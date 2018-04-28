from transports import get_transport, TransportConnetionError


STATUS_COMPLIANT = 1  # совместимо
STATUS_NOT_COMPLIANT = 2  # несовместимо
STATUS_NOT_APPLICABLE = 3  # неприменимо (отствует транспорт)
STATUS_ERROR = 4  # ошибка обработаная скриптом


def main():
    cmnd = 'if [ -f "%s" ]; then echo "Exist"; fi'
    filename = "testfile"

    try:
        transport = get_transport("SSH")
    except TransportConnetionError:
        return STATUS_NOT_APPLICABLE

    result = transport.exec(cmnd % filename)

    if "Exist" in result:
        return STATUS_COMPLIANT
    elif result == "":
        return STATUS_NOT_COMPLIANT
    else:
        return STATUS_ERROR

