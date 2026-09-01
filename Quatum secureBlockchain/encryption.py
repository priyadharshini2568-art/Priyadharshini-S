from Crypto.Cipher import AES
import hashlib
from bb84 import generate_shared_key

# -----------------------------------
# Generate AES-256 Key from BB84
# -----------------------------------

def generate_aes_key(shared_key):
    return hashlib.sha256(shared_key.encode()).digest()

# -----------------------------------
# Encrypt Message
# -----------------------------------

def encrypt_message(message, shared_key):

    aes_key = generate_aes_key(shared_key)

    cipher = AES.new(aes_key, AES.MODE_GCM)

    ciphertext, tag = cipher.encrypt_and_digest(message.encode())

    return ciphertext, cipher.nonce, tag

# -----------------------------------
# Decrypt Message
# -----------------------------------

def decrypt_message(ciphertext, nonce, tag, shared_key):

    aes_key = generate_aes_key(shared_key)

    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)

    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    return plaintext.decode()

# -----------------------------------
# Testing
# -----------------------------------

if __name__ == "__main__":

    print("\n========== AES MODULE ==========\n")

    shared_key = generate_shared_key()

    print("\nShared Key :", shared_key)

    message = input("\nEnter Message : ")

    ciphertext, nonce, tag = encrypt_message(message, shared_key)

    print("\nEncrypted Message :")
    print(ciphertext.hex())

    decrypted = decrypt_message(ciphertext, nonce, tag, shared_key)

    print("\nDecrypted Message :")
    print(decrypted)

    print("\nAES Encryption Successful")