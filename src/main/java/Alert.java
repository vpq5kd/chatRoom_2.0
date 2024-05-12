import javafx.scene.control.Label;

public class Alert {
    public void Alert(Label label, String message){
        label.setStyle("-fx-text-fill: red");
        label.setText(message);
    }
}
