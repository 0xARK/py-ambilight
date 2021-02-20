# nice -n 19 python3 stream.py

import binascii
import subprocess
import time
import cv2

from mss import mss

from PIL import Image
from PIL import ImageColor
import numpy as np
import scipy.cluster
from lasts_and_tests import util


# stream desktop screen and process with color


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
        resize_base = 50

        # don't edit these variables
        ratio = swidth / sheight
        resize_ratio = int(resize_base // ratio)

        # mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        mon = sct.monitors[0]
        last_color = [0, 0, 0]

        while True:
            # i = 0
            # for i in range(100):

            # grab image
            last_time = time.time()
            img = sct.grab(mon)

            # calcul current dominant color
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            img = img.resize((resize_base, resize_ratio))
            img.save("tmp.jpeg", "JPEG")
            colors = get("tmp.jpeg")
            rgb = []
            for key, value in colors["colors"].items():
                rgb.append(ImageColor.getcolor(value, "RGB"))
            #palette(rgb, True)

            num_clusters = 1

            im = Image.open('tmp.jpeg')
            im = im.resize((150, 150))  # optional, to reduce time
            ar = np.asarray(im)
            shape = ar.shape
            ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

            codes, dist = scipy.cluster.vq.kmeans(ar, num_clusters)

            vecs, dist = scipy.cluster.vq.vq(ar, codes)  # assign codes
            counts, bins = np.histogram(vecs, len(codes))  # count occurrences

            index_max = np.argmax(counts)  # find most frequent
            peak = codes[index_max]
            colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
            m = ImageColor.getcolor("#" + colour, "RGB")

            close = 0
            index = 0

            for i in range(5):
                diffRed = abs(rgb[i][0] - m[0])/255
                diffGreen = abs(rgb[i][1] - m[1])/255
                diffBlue = abs(rgb[i][2] - m[2])/255
                p = (diffRed + diffGreen + diffBlue)/3 * 100
                if p > close:
                    index = i

            palette([rgb[index], (m[0], m[1], m[2])], True)

            # fps calculation and exit
            print("{:.2f}".format(1 / (time.time() - last_time)) + " fps", end='\r')
            fps.append(1 / (time.time() - last_time))

            if cv2.waitKey(25) == ord('q'):
                cv2.destroyAllWindows()
                time.sleep(1)
                break

    fps = np.array(fps)
    print('median fps: {0}'.format(np.median(a=fps)))


def palette(rgb, background=False, legend=[]):
    """Generate a palette from the colors."""
    n = len(rgb)

    for i in range(0, n * 2):
        if i % n == 0:
            print()

        if legend:
            print("\033[%s8;2;%s;%s;%sm%s\033[0m" % (
            4 if background else 3, rgb[round(i % n)][0], rgb[round(i % n)][1], rgb[round(i % n)][2], " " * (80 // 20)),
                  end=" " + legend[i % n] + " ")
        else:
            print("\033[%s8;2;%s;%s;%sm%s\033[0m" % (
            4 if background else 3, rgb[round(i % n)][0], rgb[round(i % n)][1], rgb[round(i % n)][2], " " * (80 // 20)),
                  end=" ")

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


'''
def get(img, light=False, module="schemer2", sat=""):
    """Generate a palette."""

    logging.info("Generating a colorscheme.")

    # Dynamically import the backend we want to use.
    # This keeps the dependencies "optional".
    try:
        __import__("backends.%s" % module)
    except ImportError:
        __import__("backends.wal")
        module = "wal"

    logging.info("Using %s backend.", module)
    module = sys.modules["backends.%s" % module]
    colors = getattr(module, "get")(img, light)
    colors = colors_to_dict(saturate_colors(colors, sat), img)

    logging.info("Generation complete.")

    return colors
'''


def gen_colors(img):
    """Generate a colorscheme using Colorz."""
    # cmd = ["./schemer2", "-format", "img::colors", "-minBright", "0", "-in"]
    cmd = ["./schemer2", "-format", "img::colors", "-in"]
    return subprocess.check_output([*cmd, img]).splitlines()


def adjust(cols, light):
    """Create palette."""
    cols.sort(key=util.rgb_to_yiq)
    raw_colors = [*cols[8:], *cols[8:]]

    return util.generic_adjust(raw_colors, light)


def get(img, light=False, sat=""):
    """Get colorscheme."""
    '''
    if not shutil.which("schemer2"):
        logging.error("Schemer2 wasn't found on your system.")
        logging.error("Try another backend. (wal --backend)")
        sys.exit(1)
    '''
    cols = [col.decode('UTF-8') for col in gen_colors(img)]
    colors = adjust(cols, light)
    return colors_to_dict(saturate_colors(colors, sat), img)


if __name__ == "__main__":
    # util.setup_logging()
    start()
