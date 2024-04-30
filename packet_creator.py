

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

    """sends a message to the server for routing"""
    def create_client_send_message_request(self,sender_id, recipient_id, recipient_message, send_time):
        return f"s-chat***{sender_id}***send-message***{recipient_id},{recipient_message},{send_time}***//".encode('utf-8')

    """sends the routed message from the server to the appropriate client"""
    def create_server_routed_message_response(self,SERVER_ID, sender_name, sender_id, message, send_time):
        return f"s-chat***{SERVER_ID}***routed-message***{sender_name},{sender_id},{message},{send_time}***//".encode('utf-8')

    """requests to start a continuous chat"""
    def create_client_continuous_chat_request(self,client_id, chat_with_id):
        return f"s-chat***{client_id}***continuous-chat***{chat_with_id}***//".encode('utf-8')
    def create_server_routed_cc_response(self,SERVER_ID,wants_to_chat_with_name, wants_to_chat_with_id):
        return f"s-chat***{SERVER_ID}***routed-cc***{wants_to_chat_with_name},{wants_to_chat_with_id}***//".encode('utf-8')

