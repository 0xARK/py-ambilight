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
import logging
import time
import config
import cv2
import numpy as np
import pygatt
import colorsys

from mss import mss
from mss.models import Size
from PIL import Image
from PIL import ImageColor
from utils import palette, get, get_lightest
from config import led_mac_address
from ble_led import Led
from apscheduler.schedulers.blocking import BlockingScheduler

led = Led("BE:FF:20:00:FE:37", "fff0", "0000fff3-0000-1000-8000-00805f9b34fb")
# adapter = pygatt.GATTToolBackend()
# adapter.start()

# device = adapter.connect("BE:FF:20:00:FE:37", 15)
seconds_interval = 0.05
minutes_interval = 0
hours_interval = 0


def start():
    """Stream desktop screen and process with image."""
    fps = []

    # adapter = pygatt.GATTToolBackend()
    # adapter.start()

    # device = adapter.connect(mac, 15)

    with mss() as sct:

        monitor = config.dimension_screen
        if config.current_screen:
            monitor = sct.monitors[0]

        ratio = config.swidth / config.sheight
        resize_ratio = int(config.resize_base // ratio)

        if True:

            # grab image, resize it and save it
            last_time = time.time()
            img = sct.grab(monitor)

            img = Image.frombytes("RGB", Size(config.resize_base, resize_ratio), img.bgra, "raw", "BGRX")

            img.save("tmp.jpeg", "JPEG")

            # get three current dominant color and convert them from hex to rgb
            rgb = get("tmp.jpeg")
            for i in range(len(rgb)):
                rgb[i] = ImageColor.getcolor(rgb[i], "RGB")

            # get color from lightest and send it to leds
            rgb, hex = get_lightest(rgb)
            palette([rgb], True)

            h, l, s = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
            # led.set_brightness(s)
            # led.set_color(hex)
            # hex = hex[1:]
            # out = [(hex[i:i + 2]) for i in range(0, len(hex), 2)]

            # device.char_write("0000fff3-0000-1000-8000-00805f9b34fb",
            #                   [0x7e, 0x00, 0x05, 0x03, int("0x" + out[0], 16), int("0x" + out[1], 16),
            #                    int("0x" + out[2], 16), 0x00, 0xef], wait_for_response=False)

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

        if True:

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

            # get color from lightest
            rgb, hex = get_lightest(rgb)
            palette([rgb], True)

            # h, s, v = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
            # led.set_brightness(100-int(v*100/256))
            led.set_color(hex)
            hex = hex[1:]
            out = [(hex[i:i + 2]) for i in range(0, len(hex), 2)]

            # device.char_write("0000fff3-0000-1000-8000-00805f9b34fb",
            #                   [0x7e, 0x00, 0x05, 0x03, int("0x" + out[0], 16), int("0x" + out[1], 16), int("0x" + out[2], 16), 0x00, 0xef], wait_for_response=False)

            # fps calculation and exit
            print("{:.2f}".format(1 / (time.time() - last_time)) + " fps", end='\r')
            fps.append(1 / (time.time() - last_time))


def stream():
    scheduler = BlockingScheduler()
    if config.force_resize:
        pass
        scheduler.add_job(start_with_resize, 'interval', seconds=seconds_interval, minutes=minutes_interval,
                          hours=hours_interval)
    else:
        pass
        scheduler.add_job(start, 'interval', seconds=seconds_interval, minutes=minutes_interval,
                          hours=hours_interval)
    scheduler.start()


if __name__ == "__main__":
    stream()
