from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

# Generate RSA Public & Private Keys
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()


# Function to Sign Message
def sign_message(message):
    if isinstance(message, str):
        message = message.encode()

    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature


# Function to Verify Signature
def verify_signature(message, signature):
    if isinstance(message, str):
        message = message.encode()

    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return True

    except InvalidSignature:
        return False


# Test Program
if __name__ == "__main__":

    msg = input("Enter Message: ")

    signature = sign_message(msg)

    print("\nDigital Signature Created Successfully!")

    result = verify_signature(msg, signature)

    if result:
        print("Signature Verification Successful.")
    else:
        print("Signature Verification Failed.")