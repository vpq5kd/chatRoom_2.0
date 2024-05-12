public class MessageHandler {
    private int serverID;
    private String messageType;
    private String messageContent;
    public void handleMessage(String message){
        splitMessage(message);
        switch(messageType){
            case "server-retrieval":
                handleServerRetrieval();
                break;
            case "invalid-credentials":
                handleInvalidCredentials();
                break;
            case "valid-credentials":
                handleValidCredentials();
                break;
        }
    }

    private void splitMessage(String message) {
        String [] parts = message.split("\\*\\*\\*");
        serverID = Integer.parseInt(parts[1]);
        messageType = parts[2];
        messageContent = parts[3];
    }
    private void handleServerRetrieval(){
        ConnectionID.ID = messageContent;
    }
    private void handleInvalidCredentials(){

    }
    private void handleValidCredentials(){

    }
}
