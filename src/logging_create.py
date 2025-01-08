# Создание логгера
import logging

logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# Создание форматера для определения формата лога
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Создание файлового хендлера для записи логов в файл
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Создание потокового хендлера для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Добавление хендлеров к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)