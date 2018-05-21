DB_FILE = "sqlite.db"
TRANSPORTS_CONFIG_FILE = "env.json"
CONTROLS_FILE = "controls.json"

# Status codes
STATUS_COMPLIANT = 1        # совместимо
STATUS_NOT_COMPLIANT = 2    # несовместимо
STATUS_NOT_APPLICABLE = 3   # неприменимо (отствует транспорт)
STATUS_ERROR = 4            # ошибка обработаная скриптом
STATUS_EXCEPTION = 5        # ошибка скрипта обработаная модулем main

# Color console
C_OKGREEN = '\033[92m'
C_WARNING = '\033[93m'
C_FAIL = '\033[91m'
C_END = '\033[0m'
C_BOLD = '\033[1m'