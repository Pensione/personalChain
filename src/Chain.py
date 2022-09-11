from datetime import date, datetime
from email import header
import hashlib as hash
import random
import time

from ecdsa import SigningKey, NIST256p, VerifyingKey
from CustomEncryption import *



class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 4
        self.block_reward = 100
        self.VERSION = "1.0; PollyChain"
    
    #Generates the genesis block with half-hardcoded data
    def generate_genesis_block(self, address):
        BLOCK_TEXT = "GENESIS BLOCK. STAY YOUNG AND INVINCIBLE."
        nonce = 0
        while True:
            nonce_string = str(nonce)
            hashed_nonce = double_hash( nonce_string )
            current_hash = double_hash( nonce_string + BLOCK_TEXT )
            if current_hash.startswith('0' * self.difficulty, 0, self.difficulty):
                break
            nonce += 1
        timestamp = str(datetime.now())
        amount = self.block_reward
        transactions = [Transaction("SYSTEM", address, amount)]
        transaction_count = len(transactions)
        merkle_root = Block.get_merkle_root(transactions)
        block_index = len( self.chain ) + 1
        genesis_block = Block(self.VERSION, current_hash, merkle_root, transactions, transaction_count, self.difficulty, timestamp, nonce, block_index)
        return genesis_block
    
    def generate_block(self, transactions, block_result):
        nonce = block_result["nonce"]
        solution = block_result["solution"]
        prev_block_hash = solution
        timestamp = str(datetime.now())
        merkle_root = Block.get_merkle_root(transactions)
        transaction_count = len(transactions)
        block_index = len(self.chain) + 1
        block = Block(self.VERSION, prev_block_hash, merkle_root, transactions, transaction_count, self.difficulty, timestamp, nonce, block_index)
        return block

    #Generating a 32-bit nonce
    def generate_nonce(self):
        random.seed()
        return random.randint(0, (2**31))
    
    def __target(self, previous_block_hash):
        nonce = 0
        while True:
            nonce_string = str(nonce)
            hashed_nonce = double_hash( nonce_string )
            target = double_hash( hashed_nonce + previous_block_hash)
            if target.startswith('0'*self.difficulty, 0, self.difficulty):
                break
                
            nonce += 1
            
        return target
    
    def mine(self):
        print("Mining the block...")
                
        #Initialize random parameters for the nonce
        header_hash = double_hash(str(self.chain[-1].block_header))
        print("Header hash:{}".format(header_hash))
        print(str(self.chain[-1].block_header))
        target = self.__target(header_hash)

        #If current target is <= than previous target hash - the puzzle is solved and the block can be appended to the blockchain
        while True:
            nonce = self.generate_nonce()
            nonce_string = str( nonce )
            hashed_nonce = double_hash( nonce_string )
            current_hash = double_hash( hashed_nonce + header_hash)
            
            if current_hash.startswith('0' * self.difficulty, 0, self.difficulty) and (int(current_hash, base = 16) <= int(target, base = 16)):
                print("\nCurrent hash: {}".format(current_hash))
                break
            
        return {"nonce":nonce, "target":target, "solution":current_hash}
    
    def transmit_block(self):
        pass
    
    def publish_block(self, block):
        self.chain.append(block)
        
    #Method used to validate the passed block's nonce + header hash. Dummy for now
    @staticmethod
    def validate_block( block ):
        return True
    
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
        self.block_index = block_index
        
        #Constants
        self.BLOCK_SIZE = "1024"
        
    def populate_block_header(self):
        block_header = {"version":self.version, "block_index": self.block_index, "previous_block": self.prev_block_hash, "merkle_root":self.merkle_root, "timestamp":self.timestamp, "difficulty":self.difficulty, "nonce":self.nonce}
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
            self.transaction_id = self.create_transaction_id()
                        
        def create_transaction_id(self):
            transaction_id = hash.sha256(bytes(f'{self.timestamp};{self.sender};{self.reciever};{self.amount}', encoding="utf-8")).hexdigest()
            return transaction_id

        