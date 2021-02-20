"""Simple script for wal api."""
import pywal
from PIL import ImageColor


def main():
    """Main function."""
    i = 0
    for i in range(10):
        # Validate image and pick a random image if a
        # directory is given below.
        image = pywal.image.get("tmp.jpg")

        # Return a dict with the palette.
        # Set quiet to 'True' to disable notifications.
        colors = pywal.colors.get(image, ".cache")
        rgb = []
        for key, value in colors["special"].items():
            rgb.append(ImageColor.getcolor(value, "RGB"))
        for key, value in colors["colors"].items():
            rgb.append(ImageColor.getcolor(value, "RGB"))
        palette(rgb, True)
        colors = pywal.colors.get("tmp.jpg")
        rgb = []
        for key, value in colors["special"].items():
            rgb.append(ImageColor.getcolor(value, "RGB"))
        for key, value in colors["colors"].items():
            rgb.append(ImageColor.getcolor(value, "RGB"))
        palette(rgb, True)


def palette(rgb, background=False, legend=[]):
    """Generate a palette from the colors."""
    n = len(rgb)

    for i in range(0, n*2):
        if i % n == 0:
            print()

        if legend:
            print("\033[%s8;2;%s;%s;%sm%s\033[0m" % (4 if background else 3, rgb[round(i%n)][0], rgb[round(i%n)][1], rgb[round(i%n)][2], " " * (80 // 20)), end=" " + legend[i%n] + " ")
        else:
            print("\033[%s8;2;%s;%s;%sm%s\033[0m" % (4 if background else 3, rgb[round(i%n)][0], rgb[round(i%n)][1], rgb[round(i%n)][2], " " * (80 // 20)), end=" ")

    print()


main()
