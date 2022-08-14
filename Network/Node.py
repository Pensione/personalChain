import sys
import textwrap
import socket

class Socket:
    
    
    def __init__(self):
        self.SOCKET_IP = socket.gethostbyname(socket.gethostname())
        self.SOCKET_PORT = 8330
        self.BUFFER_SIZE = 1024
        self.CONNECTION_COUNT = 5
    
    @staticmethod
    def get_socket_ip():
        return socket.gethostbyname(socket.gethostname())
    
    @staticmethod
    def get_data(sock_ip, sock_port, command, **kwargs):
        with socket.socket( socket.AF_INET, socket.SOCK_STREAM) as s:
            if "timeout" in kwargs:
                s.settimeout(timeout)
            try:
                s.connect((sock_ip, sock_port))
                s.sendall(bytes(command, encoding="utf-8"))
                data = s.recv(1024)
                data_decoded = data.decode(encoding="utf-8")
            except:
                data_decoded = ''
            s.close()
            return data_decoded
    
    @staticmethod
    def set_listening_socket(sock_ip, sock_port):
        with socket.socket( socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((sock_ip, sock_port))
            print(f'Binded on: {sock_ip}:{sock_port}')
            s.listen(CONNECTION_COUNT)

            conn, address = s.accept()
            return conn


#Command constants
GET_CHAIN_DATA = "GET_CHAIN_DATA"
GET_PENDING_TRANSACTIONS = "GET_PENDING_TRANSACTIONS"
POST_TRANSACTION = "POST_TRANSACTION"

#Command responses
SUCCESS = "S"

#Networking constants
sock = Socket()
SOCK_IP = sock.SOCKET_IP
TRUSTED_IPS = ["192.168.81.82", "192.168.81.87", "192.168.81.175"]
SOCK_PORT = sock.SOCKET_PORT
BUFFER_SIZE = sock.BUFFER_SIZE
CONNECTION_COUNT = sock.CONNECTION_COUNT

print( textwrap.dedent("""Welcome to the blockhain node software!\n"""))

node_open = True
pending_transactions = []

#Trying to fetch the current latest version of the blockchain from a predefined list of trusted nodes
for ip in TRUSTED_IPS:
    try:
        print(f'Fetching data from: {ip}:{SOCK_PORT}')
        chain_data = sock.get_data(ip, SOCK_PORT, GET_CHAIN_DATA, timeout = 10)
    except:
        print("No response from the remote host!\n\n")
        continue
    
        
        
conn = sock.set_listening_socket(SOCK_IP, SOCK_PORT)

while node_open:
    with conn:
        while True:
            data = conn.recv( BUFFER_SIZE )
            data_decoded = data.decode( encoding="utf-8")
            
            if not data:
                break

            elif data_decoded == GET_CHAIN_DATA:
                conn.sendall( bytes('', encoding="utf-8"))
                break
            
            elif data_decoded == GET_PENDING_TRANSACTIONS:
                conn.sendall( bytes(str(pending_transactions), encoding="utf-8"))
                break
            
            elif data_decoded == POST_TRANSACTIONS:
                pending_transactions.append(data_decoded)
                conn.sendall( bytes(SUCCESS, encoding="utf-8"))
                break
            else:
                conn.sendall(bytes('', encoding="utf-8"))
                break



         
       