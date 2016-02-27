import random
import string


def generate_password():
    return ''.join(random.choice(string.ascii_uppercase +
                                 string.ascii_lowercase +
                                 string.digits +
                                 '#$%?!') for _ in range(10))









