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


def gen_colors(img):
    """Generate a colorscheme using Colorz."""
    # cmd = ["./lib/bin/schemer2", "-format", "img::colors", "-minBright", "0", "-in"]
    cmd = ["./lib/bin/schemer2", "-format", "img::colors", "-in"]
    colors = subprocess.check_output([*cmd, img]).splitlines()
    return colors
