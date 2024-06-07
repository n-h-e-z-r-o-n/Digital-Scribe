from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)
print(key)

import requests
url = "https://raw.githubusercontent.com/ice-black/Digital-Scribe/main/Data_Raw/system.keys.json"
response = requests.get(url)
print(response.content)
cipher_suite = Fernet(response.content)





def encrypt(text):
    encoded_text = text.encode()
    encrypted_text = cipher_suite.encrypt(encoded_text)
    return encrypted_text

def decrypt(encrypted_text):
    decrypted_text = cipher_suite.decrypt(encrypted_text)
    return decrypted_text.decode()

# Example usage
original_text = "Hello, World!"

# Encrypt
encrypted_text = encrypt(original_text)
print("Encrypted:", encrypted_text)

# Decrypt
decrypted_text = decrypt(encrypted_text)
print("Decrypted:", decrypted_text)