from cgitb import text
from datetime import datetime
import sys
import textwrap
import json
import os

from Wallet import Wallet
from Modules.FileModule import File


from ecdsa import SigningKey, NIST256p, VerifyingKey

#Directory constants
TEMP_PATH = "temp"
MINER_ADDRESS_FILE = "miner_pk.json"

if __name__ == "__main__":
    user_options = ['1', '2', '3']
    user_option = 0
    
    print(textwrap.dedent("""\
                ***************** Welcome to the NodeChain 1.0! *****************
                You are currently using the mining software. Before you start mining you should first generate a wallet address.
                If you want to proceed to the wallet - please open Wallet.py.
                
                """))
    
    
    while user_option not in user_options:
        print( textwrap.dedent("""\
            1. Start mining
            2. Change mining wallet address
            3. Exit
            
            """))
        user_option = str(input())
        
        if user_option == '1':
            File.create_or_validate( TEMP_PATH )
            temp_dir = File.get_current_dir( TEMP_PATH )
            
            #Checks whether the miner's address is already present in the miner_pk.json file
            addr_exists = File.check_file_existence( temp_dir, MINER_ADDRESS_FILE)
            
            if addr_exists:
                file = open( os.path.join( temp_dir, MINER_ADDRESS_FILE ), "r")
                json_file = json.load( file )
                miner_addr = json_file["miner_address"]
                
            else:
                print( textwrap.dedent("""\
                    Please enter your wallet's address below.
                    All the funds you recieve from the successfully mined blocks will be sent to that exact address.
                    (You can always change it if necessarry)
                    """))     
                   
                miner_addr = str(input())
                addr_valid = Wallet.validate_public_key( miner_addr )
                
                if addr_valid:
                    json_dict = {"miner_address":miner_addr}
                    json_string = json.dumps( json_dict )
                    file = open( os.path.join( temp_dir, MINER_ADDRESS_FILE), "w")
                    file.write( json_string )
                else:
                    print("Invalid address! ")
                    user_option = 0
            
            
    
        elif user_option == '2':
            pass
        
        elif user_option == '3':
            sys.exit()