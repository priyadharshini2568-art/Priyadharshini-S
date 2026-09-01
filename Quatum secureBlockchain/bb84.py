import random


def generate_shared_key(n=16, eve_attack=False):

    # Alice generates random bits and bases
    alice_bits = [random.randint(0, 1) for _ in range(n)]
    alice_bases = [random.choice(['Z', 'X']) for _ in range(n)]

    # Eve (if attack is enabled)
    if eve_attack:
        eve_bases = [random.choice(['Z', 'X']) for _ in range(n)]
    else:
        eve_bases = alice_bases[:]   # No interception

    # Eve measures
    eve_bits = []

    for i in range(n):

        if alice_bases[i] == eve_bases[i]:
            eve_bits.append(alice_bits[i])

        else:
            eve_bits.append(random.randint(0, 1))

    # Bob chooses bases
    bob_bases = [random.choice(['Z', 'X']) for _ in range(n)]

    # Bob measures
    bob_bits = []

    for i in range(n):

        if eve_bases[i] == bob_bases[i]:
            bob_bits.append(eve_bits[i])

        else:
            bob_bits.append(random.randint(0, 1))

    # Shared Key
    shared_key = []

    for i in range(n):

        if alice_bases[i] == bob_bases[i]:
            shared_key.append(bob_bits[i])

    # Error Detection
    error_count = 0

    checked_bits = 0

    for i in range(n):

        if alice_bases[i] == bob_bases[i]:

            checked_bits += 1

            if alice_bits[i] != bob_bits[i]:
                error_count += 1

    secure = (error_count == 0)

    print("\n========== BB84 PROTOCOL ==========")
    print("Alice Bits  :", alice_bits)
    print("Alice Bases :", alice_bases)

    if eve_attack:
        print("Eve Bases   :", eve_bases)
        print("Eve Bits    :", eve_bits)

    print("Bob Bases   :", bob_bases)
    print("Bob Bits    :", bob_bits)
    print("Shared Key  :", shared_key)
    print("Errors      :", error_count)

    if secure:
        print("\n✅ Quantum Key Verified")
        print("✅ No Eavesdropping Detected")
    else:
        print("\n❌ Eavesdropping Detected!")
        print("❌ Secure Communication Failed")

    return ''.join(map(str, shared_key)), secure


if __name__ == "__main__":

    key, status = generate_shared_key(eve_attack=False)

    print("\nGenerated Shared Key:", key)
    print("Secure:", status)