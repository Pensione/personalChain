
import textwrap
import socket, pickle
import sys, os

from Chain import Blockchain
from CustomEncryption import *

class Socket:
    
    def __init__(self):
        self.SOCKET_IP = socket.gethostbyname(socket.gethostname())
        self.SOCKET_PORT = 8330
        self.BUFFER_SIZE = 64000
        self.CONNECTION_COUNT = 5
    
    @staticmethod
    def execute_command(sock_ip, sock_port, command, **kwargs):
        with socket.socket( socket.AF_INET, socket.SOCK_STREAM) as s:
            if "timeout" in kwargs.keys():
                s.settimeout(kwargs["timeout"])
            try:
                requestData = {}
                requestData["command"] = command
                if "payload" in kwargs.keys():
                    requestData["payload"] = kwargs["payload"]
                else:
                    requestData["payload"] = '' 
                    
                s.connect((sock_ip, sock_port))
                s.sendall(bytes(str(requestData), encoding="utf-8"))
                data = s.recv(1024)
                data_decoded = data.decode("utf-8")
            except Exception as e:
                print(e)
                data_decoded = ''
            s.close()
            return data_decoded
    
    @staticmethod
    def set_listening_socket(sock_ip, sock_port):
        pass
        
        
#Command constants
GET_CHAIN_DATA = "GET_CHAIN_DATA"
GET_BLOCK_DATA = "GET_BLOCK_DATA"
GET_PENDING_TRANSACTIONS = "GET_PENDING_TRANSACTIONS"
POST_TRANSACTION = "POST_TRANSACTION"
POST_BLOCK = "POST_BLOCK"

#Command responses
RESPONSE_SUCCESS = "S"
RESPONSE_FAILURE = "F"

#Networking constants
sock = Socket()
SOCK_IP = sock.SOCKET_IP
TRUSTED_IPS = []
SOCK_PORT = sock.SOCKET_PORT
BUFFER_SIZE = sock.BUFFER_SIZE
CONNECTION_COUNT = sock.CONNECTION_COUNT



if __name__ == "__main__":
    
    os.system('cls')
    print( textwrap.dedent("""Welcome to the blockhain node software!\n"""))
    
    node_open = True
    chain = Blockchain()
    pending_transactions = []

    #Trying to fetch the current latest version of the blockchain from a predefined list of trusted nodes
    #for ip in TRUSTED_IPS:
    #    try:
    #        print(f'Fetching data from: {ip}:{SOCK_PORT}')
    #        chain = sock.execute_command(ip, SOCK_PORT, GET_CHAIN_DATA, timeout = 10)
    #    except:
    #        print("No response from the remote host!\n\n")
    #        continue
    #    finally:
    #        chain = Blockchain() if chain == None or chain == '' else chain
        
    

    while node_open:
        with socket.socket( socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((SOCK_IP, SOCK_PORT))
            print(f'Binded on: {SOCK_IP}:{SOCK_PORT}')
            
            s.listen(CONNECTION_COUNT)
            
            conn, address = s.accept()
            
            with conn:
                while True:
                    
                    data = conn.recv( BUFFER_SIZE )
                    if not data:
                        continue
                    print(data.decode("utf-8"))
                    try:
                        data_decoded = eval(data.decode("utf-8"))
                        command = data_decoded["command"]
                        payload = data_decoded["payload"]
                            
                        print("On main route!")
                        
                        #Sends the data of the latest block
                        if command == GET_BLOCK_DATA:
                            last_block = chain.chain[-1]
                            conn.sendall( bytes(last_block, encoding="utf-8"))
                            break
                            
                        #Sends pending transactions from the mempool
                        elif command == GET_PENDING_TRANSACTIONS:
                            conn.sendall( bytes(str(pending_transactions), encoding="utf-8"))
                            break
                            
                        elif command == GET_CHAIN_DATA:
                            conn.sendall( bytes(str(chain_data), encoding = "utf-8"))
                            break
                            
                        elif command == POST_BLOCK:
                            #Formats the payload data into an appropriate object structure
                            block = pickle.loads( payload )
                            
                            if Blockchain.validate_block(block):
                                chain.publish_block(block)
                                response_message = RESPONSE_SUCCESS
                            else:
                                response_message = RESPONSE_FAILURE
                                
                            conn.sendall(bytes(response_message, encoding="utf-8"))
                            
                            break
                        
                        elif command == POST_TRANSACTION:
                            payload = eval( payload )
                            transaction = pickle.loads( payload["transaction"])
                            sender = transaction.sender
                            signature = payload["signature"]
                            vk = vk_hex_to_bytes(sender, NIST256p)
                            valid = vk.verify( signature, payload["transaction"] )
                            response = RESPONSE_SUCCESS if valid else RESPONSE_FAILURE
                            print(f'\nSender:{transaction.sender}, reciever:{transaction.reciever}, amount:{transaction.amount}, valid:{valid}')
                            conn.sendall( bytes(response, encoding="utf-8"))
                            continue
                        else:
                            conn.sendall(bytes('NOT A VALID COMMAND', encoding="utf-8"))
                            continue
                    except Exception as e:
                        print("On exception route! Exception:{}".format(e))
                        conn.sendall(bytes("\nINVALID COMMAND SYNTHAX", encoding = "utf-8"))
                        continue


       