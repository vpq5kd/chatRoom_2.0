

"""creates a packet for sending"""
class packet_creator():
    def __init__(self):
        pass
    def create_server_name_retrieval(self):
        return (f"s-chat***server-retrieval***//").encode('utf-8')
    def create_server_name_send(self,name):
        return f"s-chat***client-name***{name}***//".encode('utf-8')
