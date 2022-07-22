from datetime import datetime
import sys
import textwrap
import json
import os
from Block import Block
from Chain import Blockchain

from Wallet import Wallet
from Modules.FileModule import File
from Network.Socket import Socket as sock

from ecdsa import SigningKey, NIST256p, VerifyingKey

#Constants(Directory e.t.c.)
TEMP_PATH = "temp"
MINER_ADDRESS_FILE = "miner_pk.json"
USER_OPTIONS = ['1', '2', '3']

#Networking constants
TRUSTED_IPS = ["192.168.81.82", "192.168.81.87", "192.168.81.175"]
MINER_IP = sock.get_socket_ip()
PORT = 8330

#Command constants
GET_CHAIN_DATA = "GET_CHAIN_DATA"


#Variables
user_option = 0


if __name__ == "__main__":
    
    
    print(textwrap.dedent("""\
                ***************** Welcome to the NodeChain 1.0! *****************
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
        
        if user_option == '1':
            
            miner_address = get_miner_address()
            if not miner_address:
                print( textwrap.dedent("""\
                    Please enter your wallet's address below.
                    All the funds you recieve from the successfully mined blocks will be sent to that exact address.
                    (You can always change it if necessarry)
                    """))
                set_miner_address()
        
            #Mining itself
            block_data = sock.get_data(MINER_IP, PORT, GET_CHAIN_DATA)
            if not block_data:
                chain = Blockchain()
                chain.generate_genesis_block()

            pass
            
    
        elif user_option == '2':
            pass
        
        elif user_option == '3':
            sys.exit()
            
            
def get_miner_address():
    File.create_or_validate( TEMP_PATH )
    temp_dir = File.get_current_dir( TEMP_PATH )
            
            #Checks whether the miner's address is already present in the miner_pk.json file
    addr_exists = File.check_file_existence( temp_dir, MINER_ADDRESS_FILE)
            
    if addr_exists:
        file = open( os.path.join( temp_dir, MINER_ADDRESS_FILE ), "r")
        json_file = json.load( file )
        miner_addr = json_file["miner_address"]
                
    else:
        miner_addr = None
                   
    return miner_addr

def set_miner_address():
    miner_addr = str(input())
    addr_valid = Wallet.validate_public_key( miner_addr )
                
    if addr_valid:
        json_dict = {"miner_address":miner_addr}
        json_string = json.dumps( json_dict )
        file = open( os.path.join( temp_dir, MINER_ADDRESS_FILE), "w")
        file.write( json_string )
    else:
        print("Invalid address!")
        user_option = 0