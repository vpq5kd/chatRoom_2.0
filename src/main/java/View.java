public enum View {
    LOGIN ("login-page.fxml"),
    COURSE_SEARCH ("course-search-scene.fxml"),
    COURSE_REVIEW("course-reviews-scene.fxml"),
    MY_REVIEW("my-reviews-scene.fxml");

    private String filename;

    View(String filename){
        this.filename = filename;
    }

    public String getFilename() {
        return filename;
    }
}
