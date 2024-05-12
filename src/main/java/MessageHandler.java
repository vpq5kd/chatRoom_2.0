public class MessageHandler {
    private int serverID;
    private String messageType;
    private String messageContent;
    public void handleMessage(String message){
        splitMessage(message);

    }

    private void splitMessage(String message) {
        String [] parts = message.split("\\*\\*\\*");
        serverID = Integer.parseInt(parts[1]);
        messageType = parts[2];
        messageContent = parts[3];
    }
}
