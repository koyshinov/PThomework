DB_FILE = "sqlite.db"
TRANSPORTS_CONFIG_FILE = "env.json"
CONTROLS_FILE = "controls.json"

# Status codes
STATUS_COMPLIANT = 1        # совместимо
STATUS_NOT_COMPLIANT = 2    # несовместимо
STATUS_NOT_APPLICABLE = 3   # неприменимо (отствует транспорт)
STATUS_ERROR = 4            # ошибка обработаная скриптом
STATUS_EXCEPTION = 5        # ошибка скрипта обработаная модулем main
