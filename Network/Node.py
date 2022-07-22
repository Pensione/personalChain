from Socket import Socket as sock
import sys


#Command constants
GET_CHAIN_DATA = "GET_CHAIN_DATA"


#Networking constants
SOCK_IP = sock.get_socket_ip()
SOCK_PORT = 8330
BUFFER_SIZE = 1024

conn = sock.set_listening_socket(SOCK_IP, SOCK_PORT)

with conn:
    while True:
        data = conn.recv( BUFFER_SIZE )
        data_decoded = data.decode( encoding="utf-8")
        
        if not data:
            break

        elif data_decoded == GET_CHAIN_DATA:
            conn.sendall( bytes("TESTDATA", encoding="utf-8"))
            
         
       