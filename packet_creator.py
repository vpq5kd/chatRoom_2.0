

"""creates a packet for sending"""
class packet_creator():
    def __init__(self):
        pass
    def create_server_name_retrieval(self,id):
        return (f"s-chat***server-retrieval***{id}***//").encode('utf-8')
    def create_server_name_send(self,id, name):
        return f"s-chat***{id}***client-name***{name}***//".encode('utf-8')
