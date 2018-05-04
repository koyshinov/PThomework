from config import STATUS_NOT_APPLICABLE, STATUS_COMPLIANT, STATUS_NOT_COMPLIANT, STATUS_ERROR
from transports import get_transport, TransportConnetionError


SQL_TABLES = "SHOW TABLES;"
SQL_SELECT = "SELECT COUNT(*) FROM testtable;"


def main():
    try:
        with get_transport("MySQL") as transport:
            tables = transport.sqlexec(SQL_TABLES)

            if not tables or "testtable" not in map(lambda x: x.get('Tables_in_sadb'), tables):
                return STATUS_NOT_COMPLIANT

            count_data = transport.sqlexec(SQL_SELECT)[0].get("COUNT(*)")

            if count_data > 0:
                return STATUS_COMPLIANT
            elif count_data == 0:
                return STATUS_NOT_COMPLIANT
            else:
                return STATUS_ERROR

    except TransportConnetionError:
        return STATUS_NOT_APPLICABLE
