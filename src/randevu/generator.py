import random
import string


def generate_code(size = 6) -> str:
    generate_pass = ''.join([random.choice( string.digits)
                                            for n in range(size)])
    return generate_pass.upper()
    