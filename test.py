import hashlib

def sha256_hash(message):
    # Преобразуем сообщение в байты
    message = message.encode('utf-8')
    # Создаём объект хеша SHA-256
    sha256 = hashlib.sha256()
    # Обновляем объект хеша байтами сообщения
    sha256.update(message)
    # Получаем шестнадцатеричное представление хеша
    hash_code = sha256.hexdigest()
    # Возвращаем хеш-код
    return hash_code


code = sha256_hash('1000Подарочная карта на 1000 рублей1rU5&meYdkBk4DPxX1731420148452DEMO')
print(code)