from flask import Flask, render_template, request
from bb84 import generate_shared_key
from encryption import encrypt_message, decrypt_message
from blockchain import Blockchain
from signature import sign_message, verify_signature

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":

        # ==========================
        # User Input
        # ==========================

        message = request.form["message"]

        # Checkbox from HTML
        eve_attack = "eve_attack" in request.form

        # Expected Receiver
        expected_receiver = "bob"

        # ==========================
        # BB84 Quantum Key
        # ==========================

        shared_key, bb84_secure = generate_shared_key(eve_attack)

        if bb84_secure:
            bb84_status = "✅ Quantum Key Verified"
        else:
            bb84_status = "❌ Eavesdropping Detected"

        # ==========================
        # AES Encryption
        # ==========================

        ciphertext, nonce, tag = encrypt_message(
            message,
            shared_key
        )

        # ==========================
        # Digital Signature
        # ==========================

        signature = sign_message(ciphertext)

        # ==========================
        # Blockchain
        # ==========================

        chain = Blockchain()

        chain.add_block(ciphertext.hex())

        blockchain_ok = chain.validate_chain()

        if blockchain_ok:
            blockchain_status = "✅ Blockchain Verified"
        else:
            blockchain_status = "❌ Blockchain Tampered"

        # ==========================
        # Signature Verification
        # ==========================

        signature_ok = verify_signature(
            ciphertext,
            signature
        )

        if signature_ok:
            signature_status = "✅ Signature Verified"
        else:
            signature_status = "❌ Signature Failed"
            # ==========================
        # Final Security Check
        # ==========================

        if expected_receiver not in message.lower():

            plaintext = "🚫 WRONG MESSAGE RECEIVED"

            final_status = "🔴 NON-SECURE COMMUNICATION<br><b>Reason:</b> Invalid Receiver"

        elif bb84_secure and blockchain_ok and signature_ok:

            plaintext = decrypt_message(
                ciphertext,
                nonce,
                tag,
                shared_key
            )

            final_status = "🟢 SECURE COMMUNICATION"

        else:

            plaintext = "🚫 WRONG MESSAGE RECEIVED"

            if not bb84_secure:

                final_status = (
                    "🔴 NON-SECURE COMMUNICATION"
                    "<br><b>Reason:</b> Eavesdropping Detected"
                )

            elif not blockchain_ok:

                final_status = (
                    "🔴 NON-SECURE COMMUNICATION"
                    "<br><b>Reason:</b> Blockchain Tampered"
                )

            else:

                final_status = (
                    "🔴 NON-SECURE COMMUNICATION"
                    "<br><b>Reason:</b> Digital Signature Verification Failed"
                )
                        # ==========================
        # Send Results to HTML
        # ==========================

        result = {
            "shared_key": shared_key,
            "bb84": bb84_status,
            "encrypted": ciphertext.hex(),
            "blockchain": blockchain_status,
            "signature": signature_status,
            "decrypted": plaintext,
            "final_status": final_status
        }

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)