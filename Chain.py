from datetime import date, datetime
from email import header
import hashlib as hash
import random
import math

from ecdsa import SigningKey, NIST256p, VerifyingKey



class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 1
        self.block_reward = 100
        self.VERSION = "1.0; PollyChain"
    
    #Generates the genesis block with half-hardcoded data
    def generate_genesis_block(self, address):
        prev_block_hash = hash.sha256(b'GENESIS BLOCK. STAY YOUNG AND INVINCIBLE.').hexdigest()
        timestamp = str(datetime.now())
        amount = self.block_reward
        transactions = [Transaction(address, "SYSTEM", amount)]
        transaction_count = len(transactions)
        merkle_root = Block.get_merkle_root(transactions)
        nonce = 0
        block_index = len( self.chain ) + 1
        genesis_block = Block(self.VERSION, prev_block_hash, merkle_root, transactions, transaction_count, self.difficulty, timestamp, nonce, block_index)
        return genesis_block
    
    def generate_block(self, transactions, nonce):
        prev_block_hash = hash.sha256(bytes(self.chain[-1].block_header["previous_block"], encoding="utf-8")).hexdigest()
        timestamp = str(datetime.now())
        merkle_root = Block.get_merkle_root(transactions)
        transaction_count = len(transactions)
        block_index = len(self.chain) + 1
        block = Block(self.VERSION, prev_block_hash, merkle_root, transactions, transaction_count, self.difficulty, timestamp, nonce, block_index)
        return block

    #Generating a 32-bit nonce
    def generate_nonce(self):
        random.seed()
        return random.randint(0, (2**31)-1)
    
    def mine(self):
        #Initialize random parameters for the target hash
        random.seed()
        target = random.randint(0, 2**(256 - self.difficulty))
        block_mined = False
        
        #Initialize random parameters for the nonce
        nonce = self.generate_nonce()
        latest_block = self.chain[-1]
        header_hash = int(latest_block.block_header["previous_block"], base = 16)
        current_hash = int(hash.sha256(bytes(str(nonce + header_hash), encoding = "utf-8")).hexdigest(), base = 16)

        #If current target is <= than previous target hash - the puzzle is solved and the block can be appended to the blockchain
        while current_hash > target:
            nonce = self.generate_nonce()
            current_hash = int(hash.sha256(bytes(str(nonce + header_hash), encoding="utf-8")).hexdigest(), base = 16)

        
        return {"nonce":nonce, "target":target, "solution":current_hash}
    
        
    def publish_block(self, block):
        self.chain.append(block)
    
class Block(Blockchain):
    
    def __init__(self, version, prev_block_hash, merkle_root, transactions, transaction_count, difficulty, timestamp, nonce, block_index):
        #Variables
        self.version = version
        self.prev_block_hash = prev_block_hash
        self.merkle_root = merkle_root
        self.difficulty = difficulty
        self.timestamp = timestamp
        self.nonce = nonce
        self.transactions = transactions
        self.transaction_count = transaction_count
        self.block_index = block_index
        self.block_header = self.populate_block_header()
        
        #Constants
        self.BLOCK_SIZE = "1024"
        
    def populate_block_header(self):
        block_header = {"version":self.version, "previous_block": self.prev_block_hash, "merkle_root":self.merkle_root, "timestamp":self.timestamp, "difficulty":self.difficulty, "nonce":self.nonce}
        return block_header
    
        
    @staticmethod
    def get_merkle_root(transactions):
        merkle_root = ""
        for entry in transactions:
            byte_entry = bytes(str(entry), encoding="utf-8")
            temp_root = merkle_root + hash.sha256(byte_entry).hexdigest()
            merkle_root = hash.sha256(bytes(temp_root, encoding="utf-8")).hexdigest()
        return merkle_root
    
          
class Transaction(Block):
    
        def __init__(self, sender, reciever, amount):
            self.sender = sender
            self.reciever = reciever
            self.amount = amount
            self.timestamp = str(datetime.now())
            self.transaction_id = self.create_transaction_id(self.timestamp, self.sender, self.reciever, self.amount)
                        
        def create_transaction_id(self, timestamp, sender, reciever, amount):
            transaction_id = hash.sha256(bytes(f'{timestamp};{sender};{reciever};{amount}', encoding="utf-8")).hexdigest()
            return transaction_id




"""
CURVE = NIST256p
sk = SigningKey.generate(curve = CURVE)
vk= sk.verifying_key
sk_string = sk.to_string()
vk_string = vk.to_string()
hex_vk = vk_string.hex()
signature = sk.sign(b"TEST MESSAGE")

print("\n" + hex_vk)
print(type(hex_vk))
print('\n')
print( type(bytes.fromhex(hex_vk)) )

new_vk = bytes.fromhex(hex_vk)
actual = VerifyingKey.from_string( new_vk, curve = CURVE)
verifoone = actual.verify(signature, b"TEST MESSAGE")
print(verifoone)
"""

"""
signature = sk.sign(b"message")
assert vk.verify(signature, b"message")

print(f'Signing key:{sk_string.hex()} \n Verifying key:{vk_string.hex()}')

parent_dir = pathlib.Path().resolve()
key_pair_dir = "Keys"

path = os.path.join(parent_dir, key_pair_dir)
os.mkdir( path )


print( "\n" + str(current_path) )"""