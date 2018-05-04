## Тестирование системы

### Подготовка

Запустить сервер (докер, виртуальную машину, ...) с установленным ssh и mysql серверами.

Убедиться, что порт ssh сервера 22022, а порт mysql сервера - 43306.

Запуск ssh сервера с помощью docker:
```commandline
docker build tests/sshd -t img-ubuntu-sshd
docker run -d -p 22022:22 --name cont-ubuntu-sshd img-ubuntu-sshd
```

Запуск mysql сервера с помощью docker:
```commandline
docker pull mariadb
docker run --name some-mariadb -p 127.0.0.1:43306:3306 -e MYSQL_ROOT_PASSWORD=pwd123 -e MYSQL_USER=sauser -e MYSQL_PASSWORD=sapassword -e MYSQL_DATABASE=sadb --rm mariadb:latest
```

Создать (поправить) конфигурационные файлы controls.json и env.json.

controls.json:
```json
{
  "001": {
    "filename": "001_test_file_exists",
    "title": "Проверка существования тестового файла",
    "requirements": "Существование файла",
    "description": "Данный тест проверяет наличие файла testfile в домашней директории пользователя root. Нужен для тестирования системы"
  },
  "002": {
    "filename": "002_test_data_in_table_exist",
    "title": "Проверка существования записей в таблице testtable",
    "requirements": "Существование записей в testtable",
    "description": "Данный тест проверяет наличие таблицы testtable и записей в таблице testtable"
  }
}

```

env.json:
```json
{
  "host": "localhost",
  "transports": {
    "SSH": {
      "login": "root",
      "password": "pwd",
      "port": 22022
    },
    "MySQL": {
      "login": "root",
      "password": "pwd123",
      "port": 43306,
      "db": "sadb"
    }
  }
}
```

### Запуск

Запуск тестов производится из директории проекта командой:
```commandline
python -m pytest tests
```

Также можно запустить один из тестов командой, например:
```commandline
python -m pytest tests/test_00_connection_ssh.py
```

### Остановка докер контейнеров

Остановить ssh сервер:
```commandline
docker container stop cont-ubuntu-sshd
docker container rm cont-ubuntu-sshd  
```

Остановить mysql сервер:
```commandline
docker container stop some-mariadb
```
