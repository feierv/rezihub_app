import random
import string

def generate_secret_key():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(50))

if __name__ == '__main__':
    secret_key = generate_secret_key()
    print(secret_key)
