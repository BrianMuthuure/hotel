import random
import string


def random_string_generator(size=4, chars=string.ascii_lowercase + string.digits):
    return f'B' + ''.join(random.choice(chars) for _ in range(size))
