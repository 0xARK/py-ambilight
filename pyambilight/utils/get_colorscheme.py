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
import os
import sys

from .adjust import adjust
from .gen_colors import gen_colors
from .saturate_colors import saturate_colors

# TODO : schemer2 detection and installation
def get_colorscheme(img, light=False, sat=""):
    """Get colorscheme."""
    if not os.path.isfile("./lib/bin/schemer2"):
        logging.error("Required dependency ./lib/bin/schemer2 does not seem to be installed.")
        sys.exit(1)
    cols = [col.decode('UTF-8') for col in gen_colors(img)]
    colors = adjust(cols, light)
    return saturate_colors(colors, sat)[1:4]
