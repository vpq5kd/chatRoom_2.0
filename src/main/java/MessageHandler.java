public class MessageHandler {
    private int serverID;
    private String messageType;
    private String messageContent;

//    public static boolean validationMessageHandled = false;
    public static String isValid;
    public void handleMessage(String message){
        splitMessage(message);
        switch(messageType){
            case "server-retrieval":
                handleServerRetrieval();
                break;
            case "invalid-credentials":
                Thread thread = new Thread(() -> {
                    synchronized (LoggedInUser.class){
                        LoggedInUser.credentialsValidated = false;
                    }

                    handleInvalidCredentials();
                });
                thread.start();
                try {
                    thread.join();
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
                break;
            case "valid-credentials":
                Thread thread1 = new Thread(() -> {
                    synchronized (LoggedInUser.class){
                        LoggedInUser.credentialsValidated = false;
                    }

                    handleValidCredentials();
                });
                thread1.start();
                try {
                    thread1.join();
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }

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
        synchronized (LoggedInUser.class){
            LoggedInUser.credentialsValidated = true;
            LoggedInUser.credentialsValid = false;
        }

    }
    private void handleValidCredentials(){
        synchronized (LoggedInUser.class){
            LoggedInUser.credentialsValidated = true;
            LoggedInUser.credentialsValid = true;
        }
    }
}
