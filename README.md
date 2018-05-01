Домашнее задание N2
===================
По стажировке в pt

Условия заданий:
- https://github.com/PTinternship/ptpy-p1
- https://github.com/PTinternship/ptpy-p2

Установка
---------

Установить докер

Создать виртуальное окружение

Установить зависимости
```
pip install -r requirements.txt
```

Тестирование
------------
Перед использованием нужно убедиться в наличии файлов (если нет, создать) `controls.json` и `env.json` и убедиться, 
что порт 23022 не используется каким-либо приложением.

Формат файла `controls.json`:
```
[
  ["000_test_file_exists", "File named 'testfile' is present in the root folder on target system."],
  ["456","some other control"]
]
```

Формат файла `env.json`:
```
{
  "host": "localhost",
  "transports": {
    "SSH": {
      "password": "pwd",
      "login": "root",
      "port": 22022
    }
  }
}
```

Чтобы тесты прошли успешно, нужно оставить скрипт `000_test_file_exists.py` в папке `script` и не изменять его.

Запуск тестов производится из директории проекта командой:
```
python -m pytest tests
```

Пример использования
--------------------
```
python main.py
```

Требования к скриптам
---------------------
- Скрипт должен находиться в папке `scripts`, быть написан на ЯП Python3 и иметь функцию run() (которая будет запускаться движком)
- Чтобы отлавливать ошибки транспорта, их нужно импортировать:
```
from transports import TransportError, UnknownTransport, TransportConnetionError
```
- Чтобы подключтиться по ssh, нужно использовать контекстный менеджер `get_transport`. Те данные, что не переданы 
  входными параметрами будут браться из файла `env.json` (Параметр `transport_name` остается обязательным). 
  Пример использования:
```
with get_transport("SSH", "localhost", 23022, "root", "pwd") as transport:
    passwd_file1 = transport.get_file("/etc/passwd")
    passwd_file2 = transport.exec("cat /etc/passwd")
``` 
  
- Пример скрипта `000_test_file_exists.py` находится в папке `scripts`
  