#imports
import socket
import threading

#global variables:
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8888

name = None
id = None

#functions:
"""creates socket"""
def create_socket():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    return client_socket

"""receives messages and sends them to handling"""
def receive_message(conn):
    while True:
        packet = conn.recv(4096).decode('utf-8')
        threading.Thread(target=handle_message, args=(packet,)).start()

"""gets the client's name, welcomes them to the application"""
def get_client_name():
    while (name == None):
        name_inputted = input("welcome to sophia's chat room, please enter your name to begin:")
        if (name_inputted):
            name = name_inputted
def handle_message(packet):
    pass
#main
def main():

    #gets the client's name for the server
    get_client_name()

    try:
        # create the client_socket
        client_socket = create_socket()

        #start listening
        threading.Thread(target=receive_message,args=(client_socket,)).start()

        #connect to server
        client_socket.connect((SERVER_ADDRESS,SERVER_PORT))

    except Exception as e:
        print(e)
