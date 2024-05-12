#imports:
import socket
import threading
import os
from packet_creator import packet_creator
from gui_database_handler import credentials_handler

#global variables
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 9999

chat_members = []

SERVER_ID = 0

pc = packet_creator()
ch = credentials_handler()


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
    def get_id(self):
        return self.id
    def __str__(self):
        return f"{self.name} ({self.id})"

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
    #translates the packet
    split_packet = packet.split("***")
    packet_type = split_packet[2]
    sender_id = split_packet[1]

    #handles the client name after the server hello
    if packet_type == "client-name":
        content = split_packet[3].split(",")
        #print(name)
        username = content[0]
        password = content[1]

        ch.add_user("admin","password") #testing purposes
        authenticated = ch.authenticate(username,password)
        print(authenticated)
        chat_member = get_member_by_id(sender_id)
        chat_member.set_name(username)
        print(chat_member.name)

    #handles the client request for
    elif packet_type == "request-users":
        chat_member = get_member_by_id(sender_id)
        users = get_members()
        users_packet = pc.create_server_actives_response(SERVER_ID,users)
        chat_member.conn.send(users_packet)

    #routes a single message to the destined client
    elif packet_type == "send-message":
        message_details = split_packet[3].split(',')

        route_member = get_member_by_id(message_details[0])
        message = message_details[1]
        send_time = message_details[2]

        send_member = get_member_by_id(sender_id)

        route_message_packet = pc.create_server_routed_message_response(SERVER_ID,send_member.name,send_member.id,message,send_time)
        route_member.conn.send(route_message_packet)

    #routes a continuous chat request to the destined client
    elif packet_type == "continuous-chat":
        requested_client_id = split_packet[3]
        requested_client = get_member_by_id(requested_client_id)
        requester = get_member_by_id(sender_id)

        routed_cc_packet = pc.create_server_routed_cc_response(SERVER_ID,requester.name,requester.id)
        requested_client.conn.send(routed_cc_packet)





    #handles a client disconnect notice
    elif packet_type == "disconnect":
        chat_member = get_member_by_id(sender_id)
        remove_member_by_id(sender_id)
        print(f"removed {chat_member.__str__()}")



"""get the chat member by ID"""
def get_member_by_id(id):
    for chat_member in chat_members:
        if chat_member.id == int(id):
            return chat_member

"""returns a list of all members"""
def get_members():
    ret_string = "\n\n"
    for chat_member in chat_members:
        ret_string+=(chat_member.__str__()+"\n")
    return ret_string

"""removes client (disconnect)"""
def remove_member_by_id(id):
    index = 0
    for chat_member in chat_members:
        if chat_member.id == int(id):
            chat_members.pop(index)
        index+=1




#main
def main():
    try:
        #creates the server
        server_socket = create_server()
        print_information()

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
            name_request = pc.create_server_name_retrieval(SERVER_ID,client_id)
            client_socket.send(name_request)

            #iterates the id
            client_id+=1


    except Exception as e:
        server_socket.close()
        print(e)
main()
