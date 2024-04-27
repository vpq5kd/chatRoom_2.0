#imports
import socket
import threading
from packet_creator import packet_creator

#global variables:
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8888

pc = packet_creator()

class client:
    def __init__(self):
        self.name = None
        self.id = None
    def set_name(self, name):
        self.name = name
    def set_id(self, id):
        self.id = id

inner_client = client()

#functions:

"""gets the client's name, welcomes them to the application"""
def get_client_name():
    while (inner_client.name == None):
        name_inputted = input("welcome to sophia's chat room, please enter your name to begin:")
        if (name_inputted):
            inner_client.set_name(name_inputted)

"""creates socket"""
def create_socket():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    return client_socket

"""receives messages and sends them to handling"""
def receive_message(conn):
    while True:
        packet = conn.recv(4096).decode('utf-8')
        threading.Thread(target=handle_message, args=(packet,conn,)).start()

"""handles the message (prints, sends, etc)"""
def handle_message(packet, conn):
    split_packet = packet.split("***")
    packet_type = split_packet[2]
    sender_id = split_packet[1]
    if packet_type == "server-retrieval":
        id = split_packet[3]
        print(id) #testing purposes
        inner_client.set_id(id)
        name_send_packet = pc.create_server_name_send(inner_client.id,inner_client.name)
        conn.send(name_send_packet)



#main
def main():

    #gets the client's name for the server
    get_client_name()

    try:
        # create the client_socket
        client_socket = create_socket()

        #connect to server
        client_socket.connect((SERVER_ADDRESS,SERVER_PORT))

        # start listening
        #receive_message(client_socket)
        threading.Thread(target=receive_message, args=(client_socket,)).start()

    except Exception as e:
        client_socket.close()
        print(e)
main()