from datetime import datetime
import sys
import textwrap
import os
import pathlib

from ecdsa import SigningKey, NIST256p, VerifyingKey
from Modules.FileModule import File

class Wallet:
    
    def __init__(self):
        self.public_key = ''
        self.private_key = ''
        self.CURVE = NIST256p
        self.KEY_PATH = "Keys"
    
    
    def create_key_pair(self):
        self.private_key = SigningKey.generate(curve = self.CURVE)
        self.public_key = self.private_key.verifying_key
        
    def save_keys(self):
        
        #Converting key pairs to hexadecimal strings
        sk_string = self.private_key.to_string().hex()
        vk_string = self.public_key.to_string().hex()
        
        #Check whether the 'Keys' directory exists, create if doesn't
        File.validate_directory( self.KEY_PATH )
        final_path = File.get_directory( self.KEY_PATH )
        
        with open( os.path.join(final_path, "keys.txt"), 'w') as key_file:
            key_file.write( f'Public key: {vk_string} \nPrivate key: {sk_string}')
            key_file.write('\n\nPlease, store your private key securely and never share it to anybody!\nOtherwise it may result in a loss of funds, wallet and identity.')
            key_file.close()
    
    @staticmethod
    def validate_public_key( key ):
        try:
            key_byte = bytes.fromhex( key )
            key_validated = VerifyingKey.from_string( key_byte, NIST256p)
            valid = True
        except Exception as e:
            valid = False
            
        return valid
            

if __name__ == "__main__":
    current_option = 0
    user_options = ['0', '1', '2', '3']
    print(
        """ ***************** Welcome to the NodeChain 1.0! *****************\n
What would you like to do? Press and enter the according number on your keyboard!
        """  
    )
    
    while current_option not in [1, 2]:
        print(
            """
1. Create a wallet.
2. Log into an existing wallet
3. Exit

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
                wallet = Wallet()
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
                
        
        elif( user_option == '2'):
            pass
        
        elif( user_option == '3'):
            sys.exit()
    

    
    