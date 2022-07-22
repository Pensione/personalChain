import socket
import sys
import random

#Networking constants
TRUSTED_IPS = ["192.168.81.82", "192.168.81.87", "192.168.81.175"]
PORT = 8330
BUFFER_SIZE = 1024
CONNECTION_COUNT = 5

#Command constants
GET_CHAIN_DATA = "GET_CHAIN_DATA"

class Socket:
    
    
    def __init__(self):
        self.SOCKET_IP = socket.gethostbyname(socket.gethostname())
        self.SOCKET_PORT = 8330
        self.BUFFER_SIZE = BUFFER_SIZE
        self.CONNECTION_COUNT = CONNECTION_COUNT
    
    @staticmethod
    def get_socket_ip():
        return socket.gethostbyname(socket.gethostname())
    
    @staticmethod
    def get_data(sock_ip, sock_port, command):
        with socket.socket( socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((sock_ip, sock_port))
            s.sendall(bytes(command, encoding="utf-8"))
            data = s.recv(1024)
            data_decoded = data.decode(encoding="utf-8")
            return data_decoded
    
    @staticmethod
    def set_listening_socket(sock_ip, sock_port):
        with socket.socket( socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((sock_ip, sock_port))
            print(f'Binded on: {sock_ip}:{sock_port}')
            s.listen(CONNECTION_COUNT)

            conn, address = s.accept()
            return conn
