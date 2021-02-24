# # # # # # # # # # # # # # # # # # # # # #
#                               _     _   #
#                              | |   (_)  #
#  _ __  _   _   __ _ _ __ ___ | |__  _   #
# | '_ \| | | | / _` | '_ ` _ \| '_ \| |  #
# | |_) | |_| || (_| | | | | | | |_) | |  #
# | .__/ \__, | \__,_|_| |_| |_|_.__/|_|  #
# | |     __/ |        by mateo castella  #
# |_|    |___/                            #
# # # # # # # # # # # # # # # # # # # # # #

# v0.5.0

# run with : nice -n 19 python3 stream.py

# TODO :  bluetooth connection, arduino support, led synchronization with wallpaper, multiscreen support ?

import cv2
import time
import numpy as np

from mss import mss
from mss.models import Size
from PIL import Image
from PIL import ImageColor
from utils import palette, get, rgb_to_hex
from config import swidth, sheight, dimension_screen, current_screen, resize_base


# stream desktop screen and process with colors
def start():

    fps = []

    with mss() as sct:

        monitor = dimension_screen
        if current_screen:
            monitor = sct.monitors[0]

        ratio = swidth / sheight
        resize_ratio = int(resize_base // ratio)

        for i in range(100):

            # grab image
            last_time = time.time()
            img = sct.grab(monitor)

            # calcul current dominant color
            img = Image.frombytes("RGB", Size(width=resize_base, height=resize_ratio), img.bgra, "raw", "BGRX")
            img.save("tmp.jpeg", "JPEG")
            rgb = get("tmp.jpeg")
            for i in range(len(rgb)):
                rgb[i] = ImageColor.getcolor(rgb[i], "RGB")
            # palette(rgb, True)

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

            last_rgb_color = rgb[index]
            last_hex_color = rgb_to_hex(rgb[index])

            # fps calculation and exit
            # print("{:.2f}".format(1 / (time.time() - last_time)) + " fps", end='\r')
            fps.append(1 / (time.time() - last_time))

            # if cv2.waitKey(25) == ord('q'):
            #     cv2.destroyAllWindows()
            #     time.sleep(1)
            #     break

    fps = np.array(fps)
    print('median fps: {0}'.format(np.median(a=fps)))


if __name__ == "__main__":
    start()
