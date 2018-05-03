# Домашнее задание N3 по стажировке в PT

Условия заданий:
- https://github.com/PTinternship/ptpy-p1
- https://github.com/PTinternship/ptpy-p2
- https://github.com/PTinternship/ptpy-p3

## Установка

Установить виртуальное окружение:
```commandline
virtualenv -p python3 venv
```

Активировать виртуальное окружение.

Установить зависимости:
```commandline
pip install -r requirements.txt
```

## Тестирование

[Документация по тестированию](tests/README.md)

Пример использования
--------------------
Консоль:
```commandline
python main.py
```

Python:
```python
from main import run
report_path = run()
```

Требования к скриптам
---------------------
- Скрипт должен находиться в папке scripts, быть написан на ЯП Python3 и иметь функцию run() (которая будет запускаться движком)
- Чтобы отлавливать ошибки транспорта, их нужно импортировать:
```python
from transports import TransportError, UnknownTransport, TransportConnetionError
```
- Чтобы подключтиться по ssh, нужно использовать контекстный менеджер get_transport. Те данные, что не переданы 
  входными параметрами будут браться из файла env.json (Параметр transport_name остается обязательным). 
  Пример использования:
```python
from transports import get_transport

with get_transport("SSH") as transport:
    passwd_file1 = transport.get_file("/etc/passwd")
    passwd_file2 = transport.exec("cat /etc/passwd")
    print(passwd_file1, passwd_file2)
``` 

- Аналогично для подключения по mysql:
```python
from transports import get_transport

SQL_SELECT = "SELECT `id`, `password` FROM `users` WHERE `email`=%s;"

with get_transport("MySQL") as transport:
    data = transport.sqlexec(SQL_SELECT, ('webmaster@python.org',))
    print(data)
```
  
- Пример скрипта 000_test_file_exists.py находится в папке scripts.
  