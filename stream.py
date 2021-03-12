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
import pygatt

from mss import mss
from mss.models import Size
from PIL import Image
from PIL import ImageColor
from utils import palette, get, get_lightest, rgb_to_hex
from config import led_mac_address


def start():
    """Stream desktop screen and process with image."""
    fps = []

    mac = "BE:FF:20:00:FE:37"
    service = "0x0011"

    adapter = pygatt.GATTToolBackend()
    adapter.start()

    device = adapter.connect(mac, 15)

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
            # palette(rgb, True)

            # get color from lightest and send it to leds
            rgb, hex = get_lightest(rgb)
            hex = hex[1:]
            out = [(hex[i:i + 2]) for i in range(0, len(hex), 2)]

            device.char_write("0000fff3-0000-1000-8000-00805f9b34fb",
                              [0x7e, 0x00, 0x05, 0x03, int("0x" + out[0], 16), int("0x" + out[1], 16),
                               int("0x" + out[2], 16), 0x00, 0xef], wait_for_response=False)

            # fps calculation and exit
            print("{:.2f}".format(1 / (time.time() - last_time)) + " fps", end='\r')
            fps.append(1 / (time.time() - last_time))


def start_with_resize():
    """Stream desktop screen and process with resized image."""
    fps = []

    mac = "BE:FF:20:00:FE:37"
    service = "0x0011"

    adapter = pygatt.GATTToolBackend()
    adapter.start()

    device = adapter.connect(mac, 15)

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
            rgb, hex = get_lightest(rgb)
            hex = hex[1:]
            out = [(hex[i:i + 2]) for i in range(0, len(hex), 2)]

            device.char_write("0000fff3-0000-1000-8000-00805f9b34fb",
                              [0x7e, 0x00, 0x05, 0x03, int("0x" + out[0], 16), int("0x" + out[1], 16), int("0x" + out[2], 16), 0x00, 0xef], wait_for_response=False)

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
