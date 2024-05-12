import java.io.*;
import java.net.Socket;

public class Connection {
    private Socket socket;
    private PrintWriter out;
    private BufferedReader in;
    public Connection(Socket conn) throws IOException {
        socket = conn;
        out = new PrintWriter(new OutputStreamWriter(socket.getOutputStream(), "UTF-8"), true);
        in = new BufferedReader(new InputStreamReader(socket.getInputStream(), "UTF-8"));

    }
    public void send(String message){
        out.println(message);
    }
    public String recv() throws IOException{
        return in.readLine();
    }
    public void close() throws IOException{
        out.close();
        in.close();
        socket.close();
    }
}
