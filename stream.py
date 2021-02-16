# nice -n 19 python3 stream.py

import time
import cv2

from mss import mss

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
        # (150, 84) ~= 27 fps ; (100, 56) ~= 31 fps ; (50, 28) ~= 36 fps ; (25, 10) ~= 38 fps
        resize_base = 150

        # don't edit these variables
        ratio = swidth/sheight
        resize_ratio = int(resize_base // ratio)

        # mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        mon = sct.monitors[0]
        last_color = [0, 0, 0]

        #while True:
        i = 0
        for i in range(5):

            # grab image
            last_time = time.time()
            img = sct.grab(mon)

            # calcul current dominant color
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "RGBX")
            img = img.resize((resize_base, resize_ratio))
            cv2.imshow("test", np.array(img))
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
            # RGB to CMYK :
            # J = max(R, G, B), c = 1 - R/J, m = 1 - G/J, y = 1 - B/J, k = 1 - J/255
            if (r*r + g*g + b*b) > color_threshold*color_threshold:
                print("replace old")
                last_color = [rgb[0], rgb[1], rgb[2]]
                j = max(rgb)
                k = int((1 - (j/255))*100)
                dark_threshold = 60
                if k > dark_threshold:
                    print("TOO DARK : ", k)
                    print("LAST RGB VALUES :", rgb)
                    r = int(255 * (1 - (1-rgb[0]/j) / 100) * (1 - dark_threshold / 100))
                    g = int(255 * (1 - (1-rgb[1]/j) / 100) * (1 - dark_threshold / 100))
                    b = int(255 * (1 - (1-rgb[2]/j) / 100) * (1 - dark_threshold / 100))
                    print("NEW RGB VALUES :", r, g, b)

            # fps calculation and exit
            fps.append(1 / (time.time() - last_time))

            if cv2.waitKey(25) == ord('q'):
                cv2.destroyAllWindows()
                time.sleep(1)
                break

    fps = np.array(fps)
    print('median fps: {0}'.format(np.median(a=fps)))


if __name__ == "__main__":
    start()
