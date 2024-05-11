import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;

import java.io.IOException;
import java.util.Objects;

public class ViewSwitcher {
    public static Scene scene;

    public static void setScene(Scene scene){
        ViewSwitcher.scene = scene;
    }

    public static void switchTo(View view) {
        try {
            FXMLLoader loader = new FXMLLoader(Objects.requireNonNull(ViewSwitcher.class.getResource(view.getFilename())));
            Parent root = loader.load();

            Object controller = loader.getController();

            scene.setRoot(root);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
