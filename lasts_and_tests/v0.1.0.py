# nice -n 19 python3 stream.py
import time
import cv2
import sys

from mss import mss
import pywal

from PIL import Image
from PIL import ImageColor
import numpy as np
import logging

# stream desktop screen and process with color
from lasts_and_tests import util


def start():

    fps = []

    with mss() as sct:

        # screen width in pixel
        swidth = 1920
        # screen height in pixel
        sheight = 1080

        # high value = low performance but high color fidelity
        # low value = high performance but we lose a little bit in colour fidelity
        # recommended value for FHD screen (1920x1080) : 150
        # highest recommended value for FHD screen (1920x1080) : 500
        # lowest recommended value for FHD screen (1920x1080) : 25
        resize_base = 500

        # don't edit these variables
        ratio = swidth / sheight
        resize_ratio = int(resize_base // ratio)

        # mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        mon = sct.monitors[0]
        # supported : wal, colorz, colorthief, haishoku, schemer2
        wal_backend = "wal"
        last_color = [0, 0, 0]

        while True:
        #i = 0
        #for i in range(100):

            # grab image
            last_time = time.time()
            img = sct.grab(mon)

            # calcul current dominant color
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            #img = img.resize((resize_base, resize_ratio))
            #os.remove("tmp.jpg")
            #os.remove(".cache/wal")
            img.save("tmp.jpeg", "JPEG")
            #cv2.imshow("test", cv2.imread("tmp.jpeg"))
            #path = pywal.image.get("tmp.jpg", ".cache")
            colors = pywal.colors.get("tmp.jpeg")
            #colorthief = ColorThief("tmp.jpg")
            #colors = colorthief.get_palette(color_count=6)
            rgb = []
            legend = []
            for key, value in colors["special"].items():
                rgb.append(ImageColor.getcolor(value, "RGB"))
                #legend.append(key)
            for key, value in colors["colors"].items():
                rgb.append(ImageColor.getcolor(value, "RGB"))
                #legend.append(key)
            palette(rgb, True, legend=[])

            # cv2.imshow("test", np.array(img))
            '''
            # calcul if current dominant color is close from old
            r = last_color[0] - rgb[0]
            g = last_color[1] - rgb[1]
            b = last_color[2] - rgb[2]
            color_threshold = 50

            # if current color not close from old, convert from RGB to CMYK and adjust color luminance for led if
            # color value is too dark
            r, g, b = rgb[0], rgb[1], rgb[2]

            if (r * r + g * g + b * b) > color_threshold * color_threshold:
                print("replace old")
                last_color = [rgb[0], rgb[1], rgb[2]]
                c, m, y, k = rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
                dark_threshold = 40
                if k > dark_threshold:
                    # print("TOO DARK : ", k)
                    # print("LAST RGB VALUES :", rgb[0], rgb[1], rgb[2])
                    r, g, b = cmyk_to_rgb(c, m, y, dark_threshold)
                    # print("NEW RGB VALUES :", r, g, b)
            '''
            # fps calculation and exit
            print("{:.2f}".format(1 / (time.time() - last_time)) + " fps", end='\r')
            fps.append(1 / (time.time() - last_time))

            if cv2.waitKey(25) == ord('q'):
                cv2.destroyAllWindows()
                time.sleep(1)
                break

    fps = np.array(fps)
    print('median fps: {0}'.format(np.median(a=fps)))


RGB_SCALE = 255
CMYK_SCALE = 100


def rgb_to_cmyk(r, g, b):
    """Convert rgb to cmyk color."""
    if (r, g, b) == (0, 0, 0):
        # black
        return 0, 0, 0, CMYK_SCALE

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / RGB_SCALE
    m = 1 - g / RGB_SCALE
    y = 1 - b / RGB_SCALE

    # extract out k [0, 1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,CMYK_SCALE]
    return int(c * CMYK_SCALE), int(m * CMYK_SCALE), int(y * CMYK_SCALE), int(k * CMYK_SCALE)


def cmyk_to_rgb(c, m, y, k, cmyk_scale=100, rgb_scale=255):
    """Convert cmyk to rgb color."""
    r = int(rgb_scale * (1.0 - c / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale)))
    g = int(rgb_scale * (1.0 - m / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale)))
    b = int(rgb_scale * (1.0 - y / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale)))
    return r, g, b


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


def colors_to_dict(colors, img):
    """Convert list of colors to pywal format."""
    return {
        "wallpaper": img,
        "alpha": util.Color.alpha_num,

        "special": {
            "background": colors[0],
            "foreground": colors[15],
            "cursor": colors[15]
        },

        "colors": {
            "color0": colors[0],
            "color1": colors[1],
            "color2": colors[2],
            "color3": colors[3],
            "color4": colors[4],
            "color5": colors[5],
            "color6": colors[6],
            "color7": colors[7],
            "color8": colors[8],
            "color9": colors[9],
            "color10": colors[10],
            "color11": colors[11],
            "color12": colors[12],
            "color13": colors[13],
            "color14": colors[14],
            "color15": colors[15]
        }
    }


def saturate_colors(colors, amount):
    """Saturate all colors."""
    if amount and float(amount) <= 1.0:
        for i, _ in enumerate(colors):
            if i not in [0, 7, 8, 15]:
                colors[i] = util.saturate_color(colors[i], float(amount))

    return colors


def get(img, light=False, backend="wal", sat=""):
    """Generate a palette."""

    logging.info("Generating a colorscheme.")

    # Dynamically import the backend we want to use.
    # This keeps the dependencies "optional".
    try:
        __import__("pywal.backends.%s" % backend)
    except ImportError:
        __import__("pywal.backends.wal")
        backend = "wal"

    logging.info("Using %s backend.", backend)
    backend = sys.modules["pywal.backends.%s" % backend]
    colors = getattr(backend, "get")(img, light)
    colors = colors_to_dict(saturate_colors(colors, sat), img)

    logging.info("Generation complete.")

    return colors


if __name__ == "__main__":
    start()
