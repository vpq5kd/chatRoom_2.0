import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import org.hibernate.Session;

import javax.persistence.TypedQuery;


public class LoginController {

    private static Session session;

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

    public void loginButtonOnAction(ActionEvent event)
    {
        String username = usernameTextField.getText();
        String password = passwordTextField.getText();

        if (username.isEmpty() || password.isEmpty()) {
            loginMessageLabel.setText("Please enter a username and password.");
            loginMessageLabel.setStyle("-fx-text-fill: red;");
            usernameTextField.clear();
            passwordTextField.clear();
            return;
        }
        /** placeholder until we add a new page and such **/
        if (userExists(username, password)) {

            LoggedInUser.username = username;

            loginMessageLabel.setText("Login successful.");
            loginMessageLabel.setStyle("-fx-text-fill: green;");
            usernameTextField.clear();
            passwordTextField.clear();


            try {
                loginMessageLabel.setText("Login successful.");
                loginMessageLabel.setStyle("-fx-text-fill: green;");
                switchToCourseSearchScene(event); // Call the scene switching method after the delay
            } catch (Exception e) {
                e.printStackTrace(); // Handle potential exceptions
            }
        } else {
            loginMessageLabel.setText("Incorrect login credentials, please try again.");
            loginMessageLabel.setStyle("-fx-text-fill: red;");
            usernameTextField.clear();
            passwordTextField.clear();
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

    private boolean userExists(String username, String password){
        Boolean UserExists = false;
        try {
            session = HibernateUtil.getSessionFactory().openSession();
            session.beginTransaction();
            String hql = "From User WHERE Username = :username AND Password = :password";
            TypedQuery<User> query = session.createQuery(hql, User.class);
            query.setParameter("username", username);
            query.setParameter("password", password);
            User user = query.getSingleResult();
            UserExists = user!=null;

        } catch (Exception e) {
            loginMessageLabel.setText("Error occurred during log-in. Please try again.");
            loginMessageLabel.setStyle("-fx-text-fill: red;");
            usernameTextField.clear();
            passwordTextField.clear();
        } finally {
            if (session != null && session.isOpen()) {
                session.close();
            }
        }
        return UserExists;
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

    public void switchToCourseSearchScene(ActionEvent event) throws Exception {
        ViewSwitcher.switchTo(View.COURSE_SEARCH);
    }

    public void exitButtonOnAction(ActionEvent event) {
        Platform.exit();
    }
}

