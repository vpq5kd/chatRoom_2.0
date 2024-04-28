import socket
from packet_creator import packet_creator
class argument_handler:
    def __init__(self, conn, id):
        self.arguments = ["--get_online","--disconnect"]
        self.conn = conn
        self.pc = packet_creator()
        self.id = id
    def get_arguments(self):
        argument = input("s-chat: ")
        self._handle_arguments(argument)
    def _handle_arguments(self, argument):
        if argument == self.arguments[0]:
            active_requests = self.pc.create_server_actives_request(self.id)
            self.conn.send(active_requests)



