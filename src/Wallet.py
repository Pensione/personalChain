from datetime import datetime
import json, pathlib, textwrap
import os, sys

from ecdsa import SigningKey, NIST256p, VerifyingKey




class Wallet():
    
    def __init__(self):
        self.KEY_PATH = os.path.join(pathlib.Path().resolve(), "Keys")
        self.public_key = self.fetch_vk_hex()
        self.private_key = self.fetch_sk_hex()
        self.CURVE = NIST256p
    
    
    ###### GETTERS ######
    
    def get_vk_hex(self):
        return self.public_key

    def get_sk_hex(self):
        return self.private_key
    
    ##### ######
    
    ###### SETTERS ######
    def create_key_pair(self):
        self.private_key = SigningKey.generate(curve = self.CURVE)
        self.public_key = self.private_key.verifying_key
        
    def save_keys(self):
        
        #Converting key pairs to hexadecimal strings
        sk_string = self.private_key.to_string().hex()
        vk_string = self.public_key.to_string().hex()
        
        
        #Check whether the 'Keys' directory exists, create if doesn't
        if not os.path.isdir( self.KEY_PATH ):
            os.mkdir( self.KEY_PATH )
        
        with open( os.path.join(self.KEY_PATH, "keys.json"), 'w') as key_file:
            bodyDict = {}
            bodyDict["PublicKey"] = vk_string
            bodyDict["PrivateKey"] = sk_string
            bodyDict["Message"] = "Please, store your private key securely and never share it to anybody! Otherwise it may result in a loss of funds, wallet and identity."
            key_file.write(json.dumps(bodyDict, indent = 4))
            key_file.close()
    
    #Assigns custom validated vk presented by user
    def set_custom_vk( self, custom_vk ):
        byte_key = bytes.fromhex( custom_vk )
        self.public_key = VerifyingKey.from_string( byte_key, self.CURVE )
        
    ##### ######
    
    def fetch_vk_hex(self):
        key_exists = self.check_key_existence()
        if key_exists:
            with open( os.path.join( self.KEY_PATH, "keys.json"), 'r') as key_file:    
                file_body = json.load( key_file )
                vk = file_body["PublicKey"]
                key_file.close()
        else:
            vk = None
                
        return vk
    
    def fetch_sk_hex(self):
        key_exists = self.check_key_existence()
        if key_exists:
            with open( os.path.join( self.KEY_PATH, "keys.json"), 'r') as key_file:
                file_body = json.load( key_file )
                sk = file_body["PrivateKey"]
                key_file.close()
        else:
            sk = None
                
        return sk
    
    #Checks if a 'keys.json' file exists in the 'Keys' directory
    def check_key_existence(self):
        KEY_FILE_NAME = "keys.json"
        file_dir = os.path.join( self.KEY_PATH, KEY_FILE_NAME)
        result = os.path.isfile( file_dir )
        return True if result else False
    
    #Validates the format of the passed public key
    @staticmethod
    def validate_public_key( key ):
        try:
            byte_key = bytes.fromhex( key )
            key_validated = VerifyingKey.from_string( byte_key, NIST256p)
            valid = True
        except Exception as e:
            valid = False
            
        return valid


if __name__ == "__main__":
    
    USER_OPTIONS = ['0', '1', '2', '3', '4']
    current_option = 0
    wallet = Wallet()
    wallet_address = wallet.fetch_vk_hex()
    
    os.system('cls')
    print(textwrap.dedent("""
    ***************** Welcome to the PollyChain 1.0! *****************\n
What would you like to do? Press and enter the according number on your keyboard!
        """)
    )
    
    while current_option not in [1, 2]:
        print(
            """
1. Create a wallet.
2. Log into an existing wallet
3. Send coins
4. Check account balance
5. Exit

            """)
        
        user_option = str(input())
        
        if user_option not in user_options:
            print("\nIncorrect input! Please choose again.")
        
        elif user_option == '0' :
            pass
        
        elif user_option == '1' :
            os.system('cls')
            print(textwrap.dedent("""\
                In terms of creating a wallet, you will recieve two keys( sequence of letters and numbers ).
                Your PUBLIC KEY is the address of your wallet. 
                    Share it with your friends, to recieve some juicy coins.
                    
                Your PRIVATE KEY should be kept COMPLETELY SECRET. 
                    It is your most important password, your only way to gain access to your wallet.
                
                If you generate a new key pair, it will be stored in the directory where you've launched your wallet from.
                You can find your key pair in the 'Keys' folder in the text file 'keys.txt'
                
                ! THE CREATION OF THE NEW WALLET WILL OVERWRITE THE EXISTING FILE WITH THE SAME NAME IN THAT DIRECTORY !
                
                Would you like to generate your key pair? (Y/N)
                """))
            choice = str(input())
            
            if choice in ['Y', 'y']:
                wallet.create_key_pair()
                wallet.save_keys()
                
                print( textwrap.dedent( """\
                    Your wallet has been successfully created!
                    Make sure you store your private key securely!
                    
                    """))
            
            elif choice in ['N', 'n']:
                pass
            
            else:
                print( "Incorrect input!")
                pass
                
        elif user_option == '2':
            pass
        
        elif user_option == '3':
            pass
        
        elif user_option == '4':
            sys.exit()
    

    
    