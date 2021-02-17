# nice -n 19 python3 stream.py
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import time
import cv2

from mss import mss
from pywal import colors as wal

from PIL import Image
from PIL import ImageColor
import numpy as np
import scipy.cluster
import binascii


# stream desktop screen and process with color
def start():
    fps = []
    num_clusters = 1

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
        resize_base = 150

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
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "RGBX")
            img = img.resize((resize_base, resize_ratio))
            # cv2.imshow("test", np.array(img))
            ar = np.asarray(img)
            shape = ar.shape

            ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

            codes, dist = scipy.cluster.vq.kmeans(ar, num_clusters)

            vecs, dist = scipy.cluster.vq.vq(ar, codes)  # assign codes
            counts, bins = np.histogram(vecs, len(codes))  # count occurrences

            peak = codes[np.argmax(counts)]  # find most frequent
            hexadecimal = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
            rgb = ImageColor.getcolor("#" + hexadecimal, "RGB")

            # calcul if current dominant color is close from old
            r = last_color[0] - rgb[0]
            g = last_color[1] - rgb[1]
            b = last_color[2] - rgb[2]
            color_threshold = 50

            # if current color not close from old, convert from RGB to CMYK and adjust color luminance for led if
            # color value is too dark
            r, g, b = rgb[0], rgb[1], rgb[2]

            if (r * r + g * g + b * b) > color_threshold * color_threshold:
                # print("replace old")
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
            print("{:.2f}".format(1 / (time.time() - last_time)) + " fps", end=' ')
            print(get_color_escape(rgb[0], rgb[1], rgb[2], True)
                  + '  '
                  + RESET + " Original color", end=' ')
            print(get_color_escape(r, g, b, True)
                  + '  '
                  + RESET + " Normalized color", end='\r')
            '''
            fps.append(1 / (time.time() - last_time))

            if cv2.waitKey(25) == ord('q'):
                cv2.destroyAllWindows()
                time.sleep(1)
                break

    fps = np.array(fps)
    print('median fps: {0}'.format(np.median(a=fps)))


RESET = '\033[0m'


def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)


RGB_SCALE = 255
CMYK_SCALE = 100


def rgb_to_cmyk(r, g, b):
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
    r = int(rgb_scale * (1.0 - c / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale)))
    g = int(rgb_scale * (1.0 - m / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale)))
    b = int(rgb_scale * (1.0 - y / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale)))
    return r, g, b


if __name__ == "__main__":
    start()
