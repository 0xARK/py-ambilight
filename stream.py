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

import time
import config
import cv2
import numpy as np
from mss import mss
from mss.models import Size
from PIL import Image
from PIL import ImageColor
from utils import palette, get, rgb_to_hex


def start():
    """Stream desktop screen and process with image."""
    fps = []

    with mss() as sct:

        monitor = config.dimension_screen
        if config.current_screen:
            monitor = sct.monitors[0]

        ratio = config.swidth / config.sheight
        resize_ratio = int(config.resize_base // ratio)

        while True:

            # grab image, resize it and save it
            last_time = time.time()
            img = sct.grab(monitor)

            img = Image.frombytes("RGB", Size(config.resize_base, resize_ratio), img.bgra, "raw", "BGRX")

            img.save("tmp.jpeg", "JPEG")

            # get three current dominant color and convert them from hex to rgb
            rgb = get("tmp.jpeg")
            for i in range(len(rgb)):
                rgb[i] = ImageColor.getcolor(rgb[i], "RGB")
            palette(rgb, True)

            # get color from lightest
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
            print("{:.2f}".format(1 / (time.time() - last_time)) + " fps", end='\r')
            fps.append(1 / (time.time() - last_time))


def start_with_resize():
    """Stream desktop screen and process with resized image."""
    fps = []

    with mss() as sct:

        monitor = config.dimension_screen
        if config.current_screen:
            monitor = sct.monitors[0]

        ratio = config.swidth / config.sheight
        resize_ratio = int(config.resize_base // ratio)

        while True:

            # grab image, resize it and save it
            last_time = time.time()
            img = sct.grab(monitor)

            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            img = img.resize((config.resize_base, resize_ratio))

            img.save("tmp.jpeg", "JPEG")

            # get three current dominant color
            rgb = get("tmp.jpeg")
            for i in range(len(rgb)):
                rgb[i] = ImageColor.getcolor(rgb[i], "RGB")
            palette(rgb, True)

            # get color from lightest
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
            print("{:.2f}".format(1 / (time.time() - last_time)) + " fps", end='\r')
            fps.append(1 / (time.time() - last_time))


def stream():
    if config.force_resize:
        start_with_resize()
    else:
        start()


if __name__ == "__main__":
    stream()
