# v0.5.0

# run with : nice -n 19 python3 stream.py

# TODO : create setup.py
# TODO : command line interface
# TODO :  bluetooth connection, clean code, arduino support, config file, multiscreen support ?

import colorsys
import cv2
from mss import mss
import numpy as np
from PIL import Image
from PIL import ImageColor
import subprocess
import time


# TODO : replace color by last_color after alt + tab bug
LAST_RGB_COLOR = [0, 0, 0]
LAST_HEX_COLOR = "#000000"


# stream desktop screen and process with colors
def start():

    fps = []

    with mss() as sct:

        # screen width in pixel
        swidth = 1920
        # screen height in pixel
        sheight = 1080

        # resize base for resize image captured and analyse it after
        # high value = low performance but high color fidelity
        # low value = high performance but we lose a little bit in colour fidelity
        # recommended value for FHD screen (1920x1080) : 150
        # highest recommended value for FHD screen (1920x1080) : 500
        # lowest recommended value for FHD screen (1920x1080) : 25
        resize_base = 50

        # monitor to capture (comment second line if you want to capture custom size on the screen)
        mon = {'top': 150, 'left': 100, 'width': 1820, 'height': 930}
        mon = sct.monitors[0]

        # don't edit these variables
        ratio = swidth / sheight
        resize_ratio = int(resize_base // ratio)

        while 1:
            # for j in range(1):

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
            palette(rgb, True)

            # get color from lighest

            last_lightest = 0
            index = 0

            # TODO : remove first color from list and iterate only on the three first colors
            # get most lightest color in the three first colors
            for i in range(4):
                indice = rgb[i][0] + rgb[i][1] + rgb[i][2]
                if indice > last_lightest:
                    last_lightest = indice
                    index = i

            LAST_RGB_COLOR = ImageColor.getcolor(rgb[index], "RGB")
            LAST_HEX_COLOR = rgb[index]

            '''
            # get color more close from cluster -> not very efficient + performance lose
            
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

            for i in range(10):
                rmean = int((rgb[i][0] + m[0]) // 2)
                r = rgb[i][0] + m[0]
                g = rgb[i][1] + m[1]
                b = rgb[i][2] + m[2]
                p = 1/math.sqrt((((512 + rmean) * r * r) >> 8) + 4 * g * g + (((767 - rmean) * b * b) >> 8))
                palette([rgb[i]], True)
                print(p)
                if p > close:
                    close = p
                    print("Closest : ")
                    palette([rgb[i]], True)
                    index = i

            # palette([rgb[index], (m[0], m[1], m[2])], True)
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


def palette(rgb, background=False, legend=[]):
    """Generate a palette from the colors."""
    n = len(rgb)

    for i in range(0, n * 2):
        if i % n == 0:
            print()

        if legend:
            print("\033[%s8;2;%s;%s;%sm%s\033[0m" % (
                4 if background else 3, rgb[round(i % n)][0], rgb[round(i % n)][1], rgb[round(i % n)][2],
                " " * (80 // 20)),
                  end=" " + legend[i % n] + " ")
        else:
            print("\033[%s8;2;%s;%s;%sm%s\033[0m" % (
                4 if background else 3, rgb[round(i % n)][0], rgb[round(i % n)][1], rgb[round(i % n)][2],
                " " * (80 // 20)),
                  end=" ")

    print()


def colors_to_dict(colors):
    """Put colors in a dict list."""
    return {
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
                colors[i] = saturate_color(colors[i], float(amount))

    return colors


def gen_colors(img):
    """Generate a colorscheme using Colorz."""
    # cmd = ["./schemer2", "-format", "img::colors", "-minBright", "0", "-in"]
    cmd = ["./schemer2", "-format", "img::colors", "-in"]
    return subprocess.check_output([*cmd, img]).splitlines()


def adjust(cols, light):
    """Create palette."""
    res = [LAST_HEX_COLOR] * 16

    try:
        cols.sort(key=rgb_to_yiq)
        raw_colors = [*cols[8:], *cols[8:]]
        res = generic_adjust(raw_colors, light)
    except:
        pass

    return res


# TODO : schemer2 detection and installation
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
    return colors_to_dict(saturate_colors(colors, sat))


def hex_to_rgb(color):
    """Convert a hex color to rgb."""
    return tuple(bytes.fromhex(color.strip("#")))


def rgb_to_hex(color):
    """Convert an rgb color to hex."""
    return "#%02x%02x%02x" % (*color,)


def rgb_to_yiq(color):
    """Sort a list of colors."""
    return colorsys.rgb_to_yiq(*hex_to_rgb(color))


def darken_color(color, amount):
    """Darken a hex color."""
    color = [int(col * (1 - amount)) for col in hex_to_rgb(color)]
    return rgb_to_hex(color)


def lighten_color(color, amount):
    """Lighten a hex color."""
    color = [int(col + (255 - col) * amount) for col in hex_to_rgb(color)]
    return rgb_to_hex(color)


def saturate_color(color, amount):
    """Saturate a hex color."""
    r, g, b = hex_to_rgb(color)
    r, g, b = [x/255.0 for x in (r, g, b)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s = amount
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    r, g, b = [x*255.0 for x in (r, g, b)]

    return rgb_to_hex((int(r), int(g), int(b)))


def generic_adjust(colors, light):
    """Generic color adjustment for themers."""
    if light:
        for color in colors:
            color = saturate_color(color, 0.60)
            color = darken_color(color, 0.5)
        colors[0] = lighten_color(colors[0], 0.95)
        colors[7] = darken_color(colors[0], 0.75)
        colors[8] = darken_color(colors[0], 0.25)
        colors[15] = colors[7]
    else:
        colors[0] = darken_color(colors[0], 0.80)
        colors[7] = lighten_color(colors[0], 0.75)
        colors[8] = lighten_color(colors[0], 0.25)
        colors[15] = colors[7]

    return colors


if __name__ == "__main__":
    start()
