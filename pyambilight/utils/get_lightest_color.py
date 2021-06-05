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

from .colortools import rgb_to_hex

def get_brightest_color_slow(rgb):
    """Get brightest color."""
    last_brightest = 0
    index = 0
    for i in range(len(rgb)):
        indice = rgb[i][0] + rgb[i][1] + rgb[i][2]
        if indice > last_brightest:
            last_brightest = indice
            index = i
    return rgb[index], rgb_to_hex(rgb[index])

def get_brightest_color(list_of_colors):
    """Get brightest color."""
    color = max(list_of_colors)
    return color, rgb_to_hex(color)

if __name__ == '__main__':
    import random
    import time

    # sample set
    print('[+] generating sample set')
    list_of_rgb_colors = [(random.randint(0,255),random.randint(0,255),random.randint(0,255)) for k in range(500000)]+[(255,255,255)]

    tic = time.time()
    r = get_brightest_color_slow(list_of_rgb_colors)
    tac = time.time()
    print("get_brightest_color_slow :",r, tac-tic)

    tic = time.time()
    r = get_brightest_color(list_of_rgb_colors)
    tac = time.time()
    print("get_brightest_color :",r, tac-tic)
