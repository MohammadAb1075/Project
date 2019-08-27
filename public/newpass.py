import random

def get_chars():
    return [chr(i) for i in range(32, 127)]


def get_forbidden_chars():
    return list(':/?#[]@!$&()*+,;=\'"\\')


def get_allowed_chars():
    return [ch for ch in get_chars() if ch not in get_forbidden_chars()]


def get_code(num):
    allowed_chars = get_allowed_chars()
    code = []
    [code.append(allowed_chars[random.randint(0, len(allowed_chars) - 1)]) for _ in range(num)]
    return ''.join(code)


# print(get_code())
# var = hashlib.sha1(b'123').hexdigest() + get_code(10)
var = get_code(10)
