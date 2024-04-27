#imports:
import socket
import threading
import os

#global variables
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8888

#classes:
"""defines a chat_member and holds data for use"""
class chat_member:
    def __init__(self,socket, address, name):
        self.conn = socket
        self.address = address
        self.name = name

#functions

"""creates the server socket and binds it to the port"""
def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    server_socket.listen(5)
    return server_socket

"""prints server information to terminal"""
def print_information():
    server_address = SERVER_ADDRESS
    server_port = SERVER_PORT
    print(f"server started on {server_address} @ {server_port}")
    print("-"*50+"\n")

#main
def main():
    try:
        server_socket = create_server()
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"accepted client {client_address}")

    except Exception as e:
        server_socket.close()
        print(e)

