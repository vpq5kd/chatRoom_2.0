#imports:
import socket
import threading
import os
from packet_creator import packet_creator

#global variables
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8888

chat_members = []

SERVER_ID = 0


#classes:
"""defines a chat_member and holds data for use"""
class chat_member:
    def __init__(self,socket, address, chat_id):
        self.conn = socket
        self.address = address
        self.id = chat_id
        self.name = None
    def set_name(self,name):
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

"""receives messages from the client and preps them for routing"""
def receive_message(conn):
    while True:
        packet = conn.recv(4096).decode('utf-8')
        threading.Thread(target=route_message, args=(packet,)).start()

"""routes the message depending on the packet"""
def route_message(packet):
    split_packet = packet.split("***")
    packet_type = split_packet[2]
    sender_id = split_packet[1]
    if packet_type == "client-name":
        name = split_packet[3]
        member = get_member_by_id(sender_id)
        member.set_name(name)

"""get the chat member by ID"""
def get_member_by_id(id):
    for member in chat_members:
        if member.id == id:
            return member




#main
def main():
    try:
        #creates the server
        server_socket = create_server()

        #accepts new clients
        client_id = 1
        while True:
            #client connection
            client_socket, client_address = server_socket.accept()
            print(f"accepted client {client_address}")

            # starts a thread to continuously listen for messages
            threading.Thread(target=receive_message, args=(client_socket,)).start()

            #creates new instance of chat_member for the client
            temp = chat_member(client_socket,client_address,client_id)
            chat_members.append(temp)


            #requests the client's name
            name_request = packet_creator.create_server_name_retrieval(SERVER_ID,client_id)
            client_socket.send(name_request)

            #iterates the id
            client_id+=1


    except Exception as e:
        server_socket.close()
        print(e)
main()
