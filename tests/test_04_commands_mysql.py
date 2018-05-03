from transports import get_transport


SQL_CREATE = '''
    CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) COLLATE utf8_bin NOT NULL,
    `password` varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
        AUTO_INCREMENT=1 ;'''

SQL_INSERT = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s);"

SQL_SELECT = "SELECT `id`, `password` FROM `users` WHERE `email`=%s;"

SQL_DELETE = "DELETE FROM `users`;"

SQL_DROP = "DROP TABLE `users`;"


def test_create_table():
    with get_transport("MySQL") as transport:
        transport.sqlexec(SQL_CREATE)


def test_insert_data():
    with get_transport("MySQL") as transport:
        data = ('webmaster@python.org', 'very-secret')
        transport.sqlexec(SQL_INSERT, data)


def test_select_data():
    with get_transport("MySQL") as transport:
        data = transport.sqlexec(SQL_SELECT, ('webmaster@python.org',))

        assert data == {'password': 'very-secret', 'id': 1}


def test_delete_data():
    with get_transport("MySQL") as transport:
        transport.sqlexec(SQL_DELETE)


def test_drop_table():
    with get_transport("MySQL") as transport:
        transport.sqlexec(SQL_DROP)
