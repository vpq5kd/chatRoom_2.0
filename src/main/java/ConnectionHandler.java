import java.io.IOException;
import java.net.Socket;

public class ConnectionHandler {
    public Socket connect(String ip, int port) throws IOException {
        Socket socket = new Socket(ip, port);
        return socket;
    }
}
