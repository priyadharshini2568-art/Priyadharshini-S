import hashlib
import datetime


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        text = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(text.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(
            len(self.chain),
            datetime.datetime.now(),
            data,
            previous_block.hash
        )
        self.chain.append(new_block)

    def display_chain(self):
        for block in self.chain:
            print("\n==============================")
            print("Block Number :", block.index)
            print("Timestamp    :", block.timestamp)
            print("Data         :", block.data)
            print("Previous Hash:", block.previous_hash)
            print("Hash         :", block.hash)

    # Tamper Detection
    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check current block hash
            if current.hash != current.calculate_hash():
                return False

            # Check previous hash link
            if current.previous_hash != previous.hash:
                return False

        return True