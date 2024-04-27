#imports:
import socket
import threading
import os
from packet_creator import packet_creator

#global variables
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8888

chat_members = []

#classes:
"""defines a chat_member and holds data for use"""
class chat_member:
    def __init__(self,socket, address):
        self.conn = socket
        self.address = address
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
def recieve_message(conn):
    while True:
        packet = conn.recv(4096).decode('utf-8')
        threading.Thread(target=route_message, args=(packet,)).start()
def route_message(packet):
    split_packet = packet.split("***")
    packet_type = split_packet[1]
    if packet_type == "client-name":


#main
def main():
    try:
        #creates the server
        server_socket = create_server()

        #starts a thread to continuously listen for messages
        threading.Thread(target=recieve_message, args=(server_socket,)).start()

        #accepts new clients
        while True:
            #client connection
            client_socket, client_address = server_socket.accept()
            print(f"accepted client {client_address}")

            #creates new instance of chat_member for the client
            temp = chat_member(client_socket,client_address)
            chat_members.append(temp)

            #requests the client's name
            name_request = packet_creator.create_server_name_retrieval()
            client_socket.send(name_request)



    except Exception as e:
        server_socket.close()
        print(e)

