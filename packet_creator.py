

"""creates a packet for sending"""
class packet_creator():
    def __init__(self):
        pass

    """Grabs the name of the client, also sends their session user-id"""
    def create_server_name_retrieval(self,server_id,client_id):
        return f"s-chat***{server_id}***server-retrieval***{client_id}***//".encode('utf-8')

    """sends the name of the client back to the server"""
    def create_server_name_send(self,id, name):
        return f"s-chat***{id}***client-name***{name}***//".encode('utf-8')

    """sends a request from the client to the server for a list of active users"""
    def create_server_actives_request(self,id):
        return f"s-chat***{id}***request-users***//".encode('utf-8')

    """sends the list of users back to the client"""
    def create_server_actives_response(self,id,users):
        return f"s-chat***{id}***retrieved-users***{users}***//".encode('utf-8')

    """sends a disconnect notice to the server"""
    def create_client_disconnect_notice(self,id):
        return f"s-chat***{id}***disconnect***//".encode('utf-8')


