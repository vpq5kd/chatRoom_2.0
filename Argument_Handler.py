#imports
import socket
import time
from packet_creator import packet_creator

#classes
class argument_handler:

    """constructor that takes in a connection and the client's id, initializes variables"""
    def __init__(self, conn, id):
        self.arguments = ["--get_online","--disconnect","--send_message"]
        self.conn = conn
        self.pc = packet_creator()
        self.id = id

    """when used in a while loop -> continuously gets messages"""
    def get_arguments(self):
        argument = input("s-chat: ")
        self._handle_arguments(argument)

    """defines the logic to execute depending on the argument"""
    def _handle_arguments(self, argument):
        if argument == self.arguments[0]:
            active_requests = self.pc.create_server_actives_request(self.id)
            self.conn.send(active_requests)
        elif argument == self.arguments[1]:
            raise KeyboardInterrupt
        elif argument == self.arguments[2]:
            recipient_id, recipient_message, send_time = self._ask_for_send_details()
            message_packet = self.pc.create_client_send_message_request(self.id, recipient_id, recipient_message, send_time)
            self.conn.send(message_packet)


    """helper method to ask for the necessary details of the message"""
    def _ask_for_send_details(self):
        recipient_id = input("recipient id: ")
        recipient_message = input("message: ")
        send_time = int(time.time())
        return recipient_id, recipient_message, send_time





