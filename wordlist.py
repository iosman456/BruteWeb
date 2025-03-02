import random
import string

def generate_password(length):
    characters = string.ascii_letters + string.digits + 'çğıöşüÇĞİÖŞÜ'
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

passwords = [generate_password(8) for _ in range(1500)]
with open('rockyou.txt', 'w') as file:
    for password in passwords:
        file.write(password + '\n')