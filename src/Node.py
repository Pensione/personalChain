
import textwrap
import socket
import sys, os
sys.path.append(os.path.abspath("modules"))
print(sys.path)

from Chain import Blockchain


class Socket:
    
    
    def __init__(self):
        self.SOCKET_IP = socket.gethostbyname(socket.gethostname())
        self.SOCKET_PORT = 8330
        self.BUFFER_SIZE = 1024
        self.CONNECTION_COUNT = 5
    
    @staticmethod
    def execute_command(sock_ip, sock_port, command, **kwargs):
        with socket.socket( socket.AF_INET, socket.SOCK_STREAM) as s:
            if "timeout" in kwargs:
                s.settimeout(timeout)
            try:
                requestData = {}
                requestData["command"] = command
                if kwargs["message_body"]:
                    requestData["payload"] = message_body
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
SUCCESS = "S"

#Networking constants
sock = Socket()
SOCK_IP = sock.SOCKET_IP
TRUSTED_IPS = ["192.168.81.82", "192.168.81.87", "192.168.81.175"]
SOCK_PORT = sock.SOCKET_PORT
BUFFER_SIZE = sock.BUFFER_SIZE
CONNECTION_COUNT = sock.CONNECTION_COUNT



if __name__ == "__main__":
    
    print( textwrap.dedent("""Welcome to the blockhain node software!\n"""))
    
    node_open = True
    chain = None
    pending_transactions = []

    #Trying to fetch the current latest version of the blockchain from a predefined list of trusted nodes
    for ip in TRUSTED_IPS:
        try:
            print(f'Fetching data from: {ip}:{SOCK_PORT}')
            chain = sock.execute_command(ip, SOCK_PORT, GET_CHAIN_DATA, timeout = 10)
        except:
            print("No response from the remote host!\n\n")
            continue
        finally:
            chain = Blockchain() if (chain == None or chain == '') else chain
        
    

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
                            conn.sendall(bytes('S',encoding="utf-8"))
                            print(data_decoded["payload"])
                            continue
                        elif command == POST_TRANSACTION:
                            pending_transactions.append(data_decoded)
                            print(pending_transactions)
                            conn.sendall( bytes(SUCCESS, encoding="utf-8"))
                            continue
                        else:
                            conn.sendall(bytes('', encoding="utf-8"))
                            continue
                    except:
                        continue


       