import hashlib
import time
import json
import logging
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 3
        self.pending_transactions = []
        self.mining_reward = 10

    
    def create_genesis_block(self):
        return Block(0, "0", time.time(), [])

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        if self.get_balance(sender) >= amount:
            transaction = {"sender": sender, "recipient": recipient, "amount": amount}
            self.pending_transactions.append(transaction)
        else:
            logging.warning("Transaction failed: Insufficient balance")

    def mine_pending_transactions(self, miner_address):
        new_block = Block(len(self.chain), self.get_latest_block().hash, time.time(), self.pending_transactions)
        self.mine_block(new_block)
        self.chain.append(new_block)
        self.pending_transactions = [{"sender": "System", "recipient": miner_address, "amount": self.mining_reward}]

    def mine_block(self, block):
        while block.hash[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        logging.info(f"Block {block.index} mined: {block.hash}")

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["recipient"] == address:
                    balance += transaction["amount"]
                if transaction["sender"] == address:
                    balance -= transaction["amount"]
        return balance

    def adjust_difficulty(self):
        if len(self.chain) > 1:
            if (self.chain[-1].timestamp - self.chain[-2].timestamp) < 10:
                self.difficulty += 1
            elif (self.chain[-1].timestamp - self.chain[-2].timestamp) > 20:
                self.difficulty -= 1

    def display_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}, Hash: {block.hash}, Transactions: {block.transactions}")

    def sync_blockchain(self, peer_url):
        response = requests.get(f"{peer_url}/get_chain")
        if response.status_code == 200:
            self.chain = response.json()

    def execute_smart_contract(self, condition, sender, recipient, amount):
        if eval(condition):  # Example: "self.get_balance('Alice') > 10"
            self.add_transaction(sender, recipient, amount)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

def generate_wallet():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, 
                                 format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return pem.decode()

# Example usage
lardcoin = Blockchain()
lardcoin.add_transaction("Alice", "Bob", 5)
lardcoin.add_transaction("Bob", "Charlie", 2)
lardcoin.mine_pending_transactions("Miner1")

print("Blockchain valid:", lardcoin.is_chain_valid())
lardcoin.display_chain()

wallet = generate_wallet()
print("Generated Wallet Address:", wallet)
