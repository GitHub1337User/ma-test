import hashlib

def md5_hash(string):
    """Функция для генерации MD5 хэша из строки."""
    return hashlib.md5(string.encode('utf-8')).hexdigest()

def generate_sign(params, token=None):
    """Генерация подписи (sign) на основе параметров."""
    # Копируем параметры
    linked_hash_map = params.copy()

    # Добавляем токен, если он существует
    if token:
        linked_hash_map['token'] = token

    # Хэшируем значения параметров
    hashes = [md5_hash(value) for value in linked_hash_map.values()]

    # Сортируем хэши в алфавитном порядке
    hashes.sort()

    # Конкатенируем с базовой строкой
    base_string = 'ABCDEF00G' + ''.join(hashes)

    # Генерируем финальную подпись
    sign = md5_hash(base_string)

    return sign

