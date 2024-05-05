from cryptography.fernet import Fernet
import json

# Generate a key
def generate_key():
    return Fernet.generate_key()

# Encrypt data
def encrypt_data(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

# Decrypt data
def decrypt_data(encrypted_data, key):
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data

# Encrypt JSON data and save to file
def encrypt_json(data, key, filename):
    encrypted_data = encrypt_data(json.dumps(data), key)
    with open(filename, 'wb') as f:
        f.write(encrypted_data)

# Decrypt JSON data from file
def decrypt_json(filename, key):
    with open(filename, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = decrypt_data(encrypted_data, key)
    return json.loads(decrypted_data)

# Example JSON data
json_data = {"name": "John", "age": 30, "city": "New York"}

# Generate a key
key = generate_key()

# Encrypt JSON data and save to file
encrypt_json(json_data, key, "encrypted_data.json")

# Decrypt JSON data from file
decrypted_data = decrypt_json("encrypted_data.json", key)
print("Decrypted JSON data:", decrypted_data)
