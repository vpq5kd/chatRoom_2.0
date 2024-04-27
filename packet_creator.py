

"""creates a packet for sending"""
class packet_creator():
    def __init__(self):
        pass
    def create_server_name_retrieval(self,server_id,client_id):
        return (f"s-chat***{server_id}***server-retrieval***{client_id}***//").encode('utf-8')
    def create_server_name_send(self,id, name):
        return f"s-chat***{id}***client-name***{name}***//".encode('utf-8')
