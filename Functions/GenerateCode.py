import random
import string

def generate_unique_code(length=9):
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(characters, k=length))
    return code
