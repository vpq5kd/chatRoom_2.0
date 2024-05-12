import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import org.hibernate.Session;

import javax.persistence.TypedQuery;
import java.net.Socket;
import java.util.regex.Pattern;


public class LoginController {

    private static Session session;
    private Socket conn;
    private Alert alert = new Alert();
    private boolean connected = false;
    public static boolean credentialsValidated = false;
    public static boolean credentialsValid = false;

    @FXML
    private Button connectButton;

    @FXML
    private TextField usernameSignUpTextField;
    @FXML
    private TextField passwordSignUpTextField;
    @FXML
    private Label signUpMessageLabel;
    @FXML
    private Button signUpButton;
    @FXML
    private Button exitButton;

    @FXML
    private TextField usernameTextField;
    @FXML
    private TextField passwordTextField;
    @FXML
    private Button loginButton;
    @FXML
    private Label loginMessageLabel;
    @FXML
    private Label loadingIn;
    @FXML
    private TextField serverAddress;
    @FXML
    private Label connectionMessageLabel;


    public void connectButtonOnAction(ActionEvent event) {
        try {
            String[] parts = serverAddress.getText().split(":");
            String ipAddress = parts[0];
            String portStr = parts[1];
            if (!isValidIp(ipAddress)) {
                connectionMessageLabel.setStyle("-fx-text-fill: red");
                connectionMessageLabel.setText("Invalid IP, please try again.");
                return;
            } else if (!isValidPort(portStr)) {
                connectionMessageLabel.setStyle("-fx-text-fill: red;");
                connectionMessageLabel.setText("Port must be a number between 0 and 65535.");
                return;
            }


            ConnectionHandler connectionHandler = new ConnectionHandler();
            try {
                conn = connectionHandler.connect(ipAddress, Integer.parseInt(portStr));
                Listener listener = new Listener(conn);
                Thread thread = new Thread(listener::listen);
                thread.start();
                connected = true;
                connectionMessageLabel.setStyle("-fx-text-fill: green");
                connectionMessageLabel.setText("Connection successful!");
            } catch (Exception e) {
                connectionMessageLabel.setStyle("-fx-text-fill: red;");
                connectionMessageLabel.setText("Connection failed, please try again.");
            }
        }catch (Exception e){
            alert.Alert(connectionMessageLabel,"something went wrong, please try again.");
            return;
        }
    }
    private boolean isValidIp(String ipAddress){
        String ipRegex = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$";
        Pattern pattern = Pattern.compile(ipRegex);
        return pattern.matcher(ipAddress).matches();
    }
    private boolean isValidPort(String port){
        try{
            int portInt = Integer.parseInt(port);
            return portInt>=0 && portInt<= 65535;
        }catch (NumberFormatException e){
            return false;
        }
    }
    public void loginButtonOnAction(ActionEvent event) {
        try {
            String username = usernameTextField.getText();
            String password = passwordTextField.getText();

            if (!connected) {
                alert.Alert(loginMessageLabel, "Please connect to a S-Chat server before logging in.");
                return;
            }

            if (username.isEmpty() || password.isEmpty()) {
                loginMessageLabel.setText("Please enter a username and password.");
                loginMessageLabel.setStyle("-fx-text-fill: red;");
                usernameTextField.clear();
                passwordTextField.clear();
                return;
            }
            userExists(username,password);
        }catch (Exception e){
            alert.Alert(loginMessageLabel,"Error during login, please try again.");
        }
    }



    public void signUpButtonOnAction(ActionEvent event) {

        String username = usernameSignUpTextField.getText();
        String password = passwordSignUpTextField.getText();

        if (username.isEmpty() || password.isEmpty()) {
            signUpMessageLabel.setText("Please enter a username and password.");
            signUpMessageLabel.setStyle("-fx-text-fill: red;");
            usernameSignUpTextField.clear();
            passwordSignUpTextField.clear();
            return;
        }

        if (password.length() < 8) {
            signUpMessageLabel.setText("Password must be at least 8 characters.");
            signUpMessageLabel.setStyle("-fx-text-fill: red;");
            usernameSignUpTextField.clear();
            passwordSignUpTextField.clear();
            return;
        }

        addUser(username, password);

        usernameSignUpTextField.clear();
        passwordSignUpTextField.clear();
    }

    private void addUser(String username, String password) {
        if (usernameExists(username)) {
            signUpMessageLabel.setText("Username in use, please try again");
            signUpMessageLabel.setStyle("-fx-text-fill: red;");
            usernameSignUpTextField.clear();
            passwordSignUpTextField.clear();
        } else {
            try {
                session = HibernateUtil.getSessionFactory().openSession();
                session.beginTransaction();

                User newUser = new User(username, password);

                session.persist(newUser);
                session.getTransaction().commit();

                signUpMessageLabel.setText("Sign up successful. Please log in.");
                signUpMessageLabel.setStyle("-fx-text-fill: green;");
                usernameSignUpTextField.clear();
                passwordSignUpTextField.clear();

            } catch (Exception e) {
                System.out.println(e.getMessage());
                signUpMessageLabel.setText("Error occurred during sign-up. Please try again.");
                signUpMessageLabel.setStyle("-fx-text-fill: red;");
                usernameSignUpTextField.clear();
                passwordSignUpTextField.clear();
            } finally {
                if (session != null && session.isOpen()) {
                    session.close();
                }
            }
        }
    }

    private void userExists(String username, String password){
        try {
            String message = "s-chat***"+ConnectionID.ID+"***"+"client-name"+"***"+username+","+password+"***//\n";
            Listener.connection.send(message);
            while(!LoggedInUser.credentialsValidated){}
            if (LoggedInUser.credentialsValid){
                alert.Success(loginMessageLabel, "login successful.");
                return;
            }

        } catch (Exception e) {
            loginMessageLabel.setText("Error occurred during log-in. Please try again.");
            loginMessageLabel.setStyle("-fx-text-fill: red;");
            usernameTextField.clear();
            passwordTextField.clear();
        }
        LoggedInUser.credentialsValidated = false;
        alert.Alert(loginMessageLabel, "Invalid credentials, please try again.");

    }

    private boolean usernameExists(String username){
        Boolean UsernameExists = false;
        try {
            session = HibernateUtil.getSessionFactory().openSession();
            session.beginTransaction();
            String hql = "From User WHERE Username = :username";
            TypedQuery<User> query = session.createQuery(hql, User.class);
            query.setParameter("username", username);
            User user = query.getSingleResult();
            UsernameExists = user!=null;

        } catch (Exception e) {
            //this is here to catch the error that is thrown if the username does not exist
            //functionally correct but if you can think of a way to do this without an empty catch block go for it
        } finally {
            if (session != null && session.isOpen()) {
                session.close();
            }
        }
        return UsernameExists;
    }


    public void exitButtonOnAction(ActionEvent event) {
        Platform.exit();
    }


}

