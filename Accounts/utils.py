import secrets
import string

def generate_unique_string(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for i in range(length))