#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import logging
import math
import time
import numpy as np
from .config import *

from mss import mss
from mss.models import Size
from PIL import Image
from PIL import ImageColor

from utils import rgb_to_hex, get, get_brightest_color


def test_fps():
    """Test image processing performance."""
    fps = []

    with mss() as sct:

        ratio = config.swidth / config.sheight
        resize_ratio = int(config.resize_base // ratio)

        monitor = config.dimension_screen

        if config.current_screen:
            monitor = sct.monitors[0]

        for i in range(100):

            print("test " + str(i + 1) + "/100", end="\r" if i < 99 else "\n")

            # grab image, resize it and save it
            last_time = time.time()
            img = sct.grab(monitor)

            if config.force_resize:
                img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
                img = img.resize((config.resize_base, resize_ratio))
            else:
                img = Image.frombytes("RGB", Size(width=config.resize_base, height=resize_ratio), img.bgra, "raw",
                                      "BGRX")

            img.save("tests/tmp_tests.jpeg", "JPEG")

            # get three current dominant color and convert them from hex to rgb
            rgb = get("tests/tmp_tests.jpeg")
            for i in range(len(rgb)):
                rgb[i] = ImageColor.getcolor(rgb[i], "RGB")

            # get color from lightest
            rgb, hex = get_brightest_color(rgb)

            # fps calculation
            fps.append(1 / (time.time() - last_time))

    fps = np.array(fps)
    median = np.median(a=fps)
    logging.info("Median fps : {:.2f}".format(np.median(a=fps)))
    if median < 10:
        logging.error("The image processing is too slow. Please use a different configuration.")
    elif median < 15:
        logging.warning("Be careful, image processing is very slow. The colours will not change in real time. Change "
                        "the configuration to improve the processing time.")
    else:
        logging.info("Image processing is going well.")


def test_color():
    """Test color detection."""
    ratio = config.swidth / config.sheight
    resize_ratio = int(config.resize_base // ratio)

    def test_one_color(text_color, rgb_color):
        """Test detection for one given color."""
        logging.info("Test detection of " + text_color + " color.")
        img = Image.open("tests/" + text_color + "_tests.jpeg")
        img = img.resize((config.resize_base, resize_ratio))
        img.save("tests/tmp_tests.jpeg", "JPEG")
        rgb = get("tests/tmp_tests.jpeg")
        for i in range(len(rgb)):
            rgb[i] = ImageColor.getcolor(rgb[i], "RGB")
        rgb, hex = get_brightest_color(rgb)
        difference = math.sqrt((rgb[0] - rgb_color[0])*(rgb[0] - rgb_color[0]) + (rgb[1] - rgb_color[1])*(rgb[1] - rgb_color[1]) + (rgb[2] - rgb_color[2])*(rgb[2] - rgb_color[2]))
        percentage = difference/math.sqrt(255 ^ 2 + 255 ^ 2 + 255 ^ 2)
        logging.info("RGB color detected : " + str(rgb))
        if percentage < 20:
            logging.info("Good, " + text_color + " has been detected with a precision of {:.2f}%".format(100-percentage))
        else:
            logging.error("Warning, " + text_color + " has been detected with an insufficient precision of {:.2f}%".format(100-percentage))
        print()

    # test white detection
    test_one_color("white", (255, 255, 255))
    # test black detection
    test_one_color("black", (0, 0, 0))
    # test red detection
    test_one_color("red", (255, 0, 0))
    # test green detection
    test_one_color("green", (0, 255, 0))
    # test blue detection
    test_one_color("blue", (0, 0, 255))


def run_tests():
    logging.info("Start tests.")
    print()
    logging.info("Start test of image processing performance.")
    print()
    test_fps()
    print()
    logging.info("Start test of color detection.")
    print()
    test_color()
