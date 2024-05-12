import java.io.IOException;
import java.net.Socket;

public class Listener {
    Connection connection;
    public Listener(Socket conn) throws IOException {
         connection = new Connection(conn);
    }

    public void listen(){
        while (true){
            try {
                String message = connection.recv();
                Thread thread = new Thread(() -> {
                    handleMessage(message);
                });
                thread.start();

            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }
    private void handleMessage(String message){
        System.out.println(message);
    }
}
