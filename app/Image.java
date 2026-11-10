public class Image {
    private int width;
    private int height;
    private String format;

    public Image() {
        width = 0;
        height = 0;
        format = "Unknown";
    }

    public Image(int width, int height) {
        this.width = width;
        this.height = height;
        format = "Unknown";
    }

    public Image(int width, int height, String format) {
        this.width = width;
        this.height = height;
        this.format = format;
    }

    public void resize(double scale) {
        width = (int) (width * scale);
        height = (int) (height * scale);
    }

    public void resize(int newWidth, int newHeight) {
        width = newWidth;
        height = newHeight;
    }

    public void printInfo() {
        System.out.println("Width: " + width);
        System.out.println("Height: " + height);
        System.out.println("Format: " + format);
    }

    public static void main(String[] args) {
        Image image1 = new Image();
        Image image2 = new Image(800, 600);
        Image image3 = new Image(1920, 1080, "PNG");

        System.out.println("Image 1:");
        image1.printInfo();

        System.out.println();

        System.out.println("Image 2:");
        image2.printInfo();

        image2.resize(2.0);

        System.out.println();
        System.out.println("Image 2 after resize:");
        image2.printInfo();

        System.out.println();

        System.out.println("Image 3:");
        image3.printInfo();

        image3.resize(1280, 720);

        System.out.println();
        System.out.println("Image 3 after resize:");
        image3.printInfo();
    }
}