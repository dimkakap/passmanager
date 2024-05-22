import os
import json
import secrets
import string
import subprocess
import sys

# Проверка и установка модуля cryptography
try:
    from cryptography.fernet import Fernet
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
    from cryptography.fernet import Fernet

# Функция для генерации ключа шифрования и сохранения его в файл
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Функция для загрузки ключа из файла
def load_key():
    return open("secret.key", "rb").read()

# Функция для шифрования пароля
def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Функция для дешифрования пароля
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

# Функция для генерации случайного пароля
def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

# Функция для сохранения зашифрованного пароля в файл
def save_password(site, encrypted_password):
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            passwords = json.load(file)
    else:
        passwords = {}
    
    passwords[site] = encrypted_password.decode()
    
    with open("passwords.json", "w") as file:
        json.dump(passwords, file)

# Функция для загрузки зашифрованного пароля из файла
def load_password(site):
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            passwords = json.load(file)
        return passwords.get(site)
    return None

# Главная функция программы
def main():
    if not os.path.exists("secret.key"):
        generate_key()
    
    key = load_key()
    
    while True:
        print("\n1. Сгенерировать случайный пароль")
        print("2. Сохранить новый пароль")
        print("3. Получить сохраненный пароль")
        print("4. Выйти")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            length = int(input("Введите длину пароля: "))
            new_password = generate_password(length)
            print(f"Сгенерированный пароль: {new_password}")
        
        elif choice == '2':
            site = input("Введите название сайта/сервиса: ")
            password = input("Введите пароль: ")
            encrypted_password = encrypt_password(password, key)
            save_password(site, encrypted_password)
            print("Пароль сохранен.")
        
        elif choice == '3':
            site = input("Введите название сайта/сервиса: ")
            encrypted_password = load_password(site)
            if encrypted_password:
                password = decrypt_password(encrypted_password.encode(), key)
                print(f"Пароль для {site}: {password}")
            else:
                print("Пароль не найден.")
        
        elif choice == '4':
            break
        
        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
