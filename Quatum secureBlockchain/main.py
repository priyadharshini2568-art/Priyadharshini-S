from bb84 import generate_shared_key
from encryption import encrypt_message, decrypt_message
from blockchain import Blockchain
from signature import sign_message, verify_signature


print("==========================================")
print(" QUANTUM SECURE BLOCKCHAIN COMMUNICATION ")
print("==========================================\n")

# Generate BB84 Shared Key
shared_key = generate_shared_key()

print("\nBB84 Shared Key Generated Successfully!\n")

# Alice enters message
message = input("Enter Message to Send: ")

# Encrypt message
ciphertext, nonce, tag = encrypt_message(message, shared_key)

print("\nEncrypted Message:")
print(ciphertext.hex())

# Create Digital Signature
signature = sign_message(ciphertext)

print("\nDigital Signature Generated Successfully!")

# Create Blockchain
chain = Blockchain()

# Store encrypted message in blockchain
chain.add_block(ciphertext.hex())

print("\nBlockchain Data\n")
chain.display_chain()
print("\nChecking Blockchain Integrity...")

if chain.validate_chain():
    print("Blockchain Verified")
    print("No Tampering Detected")
else:
    print("Blockchain Tampered!")
    print("Communication Not Secure!"                                                                                                                   )

# Verify Digital Signature
if verify_signature(ciphertext, signature):
    print("\nDigital Signature Verified Successfully!")
else:
    print("\nDigital Signature Verification Failed!")

# Bob decrypts message
plaintext = decrypt_message(ciphertext, nonce, tag, shared_key)

print("\nBob Received Message:")
print(plaintext)

print("\nSecure Communication Completed Successfully!")