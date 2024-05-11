import javax.persistence.*;

@Entity
@Table(name="USERS")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column (name = "ID")
    private int id;

    @Column(name = "Username", unique = true, nullable = false)
    private String Username;

    @Column(name = "Password", nullable = false)
    private String Password;

    public User(String username, String password) {
        this.Username = username;
        this.Password = password;
    }

    public User() {
    }

    public String getUsername() {
        return Username;
    }

    public void setUsername(String username) {
        this.Username = username;
    }

    public String getPassword() {
        return Password;
    }

    public void setPassword(String password) {
        this.Password = password;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

}
