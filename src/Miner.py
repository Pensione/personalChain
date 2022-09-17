from socket import timeout
import textwrap
import json
import os, sys, pathlib, pickle

from Chain import Blockchain, Block, Transaction

from Wallet import Wallet
from Node import Socket

from ecdsa import SigningKey, NIST256p, VerifyingKey



#Constants(Directory e.t.c.)
USER_OPTIONS = ['1', '2', '3']
KEY_PATH = os.path.join(pathlib.Path().resolve(), "Keys")
LOG_FILE_NAME = "sample.json"

#Networking constants
sock = Socket()
MINER_IP = sock.SOCKET_IP
TRUSTED_IPS = [ "192.168.1.104"]
PORT = 8330

#Command constants
GET_CHAIN_DATA = "GET_CHAIN_DATA"
GET_BLOCK_DATA = "GET_BLOCK_DATA"
GET_PENDING_TRANSACTIONS = "GET_PENDING_TRANSACTIONS"
POST_BLOCK = "POST_BLOCK"
POST_TRANSACTION = "POST_TRANSACTION"

#Variables
user_option = 0


def mine(blockchain, miner_address, genesis_required):
    while True:
        if genesis_required:
            genesis_block = blockchain.generate_genesis_block(miner_address)
            blockchain.publish_block(genesis_block)
            genesis_required = False
            log_block_data(genesis_block)
            continue

        block_result = blockchain.mine()
        
        #Fetch the list of pending transactions from the available nodes
        pending_transactions = sock.execute_command(MINER_IP, PORT, GET_PENDING_TRANSACTIONS, timeout = 1)
        transaction_list = []
        
        #Generate the system -> miner transaction and collect transactions from pending_transactions
        coinbase_transaction = Transaction("SYSTEM", miner_address, blockchain.block_reward)
        transaction_list.append( coinbase_transaction )
        if pending_transactions:
            transaction_list.append( transaction for transaction in pending_transactions)
            
        new_block = blockchain.generate_block(transaction_list, block_result)
        
        #Convert the object data into a string before sending it as a bytestream
        block_data_string = pickle.dumps(new_block)
        
        for ip in TRUSTED_IPS:
            print(sock.execute_command(ip, PORT, POST_BLOCK, payload = block_data_string, timeout = 1))
            
        blockchain.publish_block(new_block)
        
        
        log_block_data(new_block)

#Logs the entire block as json into the sample.json file in the 'Keys' directory
def log_block_data(block):
    rootData = {}
    rootData["block_header"] = block.block_header
    rootData["block_size"] = block.BLOCK_SIZE
    rootData["transaction_count"] = block.transaction_count
    rootData["transactions"] = []
    transaction_list = block.transactions
    for entry in transaction_list:
        transaction = entry.__dict__
        rootData["transactions"].append(transaction)
    
    json_data = json.dumps(rootData, indent = 4)
    with open( os.path.join( KEY_PATH, LOG_FILE_NAME), 'a' ) as log_file:
        log_file.write('\n' + str(json_data) + ',')
        log_file.close()


def get_pending_transactions():
    pass


if __name__ == "__main__":
    
    
    print(textwrap.dedent("""\
                ***************** Welcome to the PollyChain 1.0! *****************
                You are currently using the mining software. Before you start mining you should first generate a wallet address.
                If you want to proceed to the wallet - please open Wallet.py.
                
                """))
    
    
    while user_option not in USER_OPTIONS:
        print( textwrap.dedent("""\
            1. Start mining
            2. Change mining wallet address
            3. Exit
            
            """))
        
        user_option = str(input())
        wallet = Wallet()
        
        if user_option == '1':
            address_exists = wallet.check_key_existence()
            
            if not address_exists:
                print( textwrap.dedent("""\
                    Please enter your wallet's address below.
                    All the funds you recieve from the successfully mined blocks will be sent to that exact address.
                    (You can always change it if necessarry)
                    """))
                custom_address = str(input())
                valid_address = Wallet.validate_public_key( custom_address )
                
                if not valid_address:
                    print( "The address you've entered is in invalid format!")
                    user_option = 0
                    continue
                    
                else:
                    wallet.set_custom_vk( custom_address )
                    wallet.save_keys()

            miner_address = wallet.get_vk_hex()
            
            #Fetching the initial chain data, to determine whether a genesis block should be created
            block_data = None #sock.execute_command(MINER_IP, PORT, GET_BLOCK_DATA)
            genesis_required = True if (block_data is None or block_data == '') else False
            chain = Blockchain()
            mine(chain, miner_address, genesis_required)
            
    
        elif user_option == '2':
            pass
        
        elif user_option == '3':
            sys.exit()
            