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


def generic_adjust(colors, light):
    """Generic color adjustment for themers."""
    if light:
        for color in colors:
            color = saturate_color(color, 0.60)
            color = darken_color(color, 0.5)
        colors[0] = lighten_color(colors[0], 0.95)
        colors[7] = darken_color(colors[0], 0.75)
        colors[8] = darken_color(colors[0], 0.25)
        colors[15] = colors[7]
    else:
        colors[0] = darken_color(colors[0], 0.80)
        colors[7] = lighten_color(colors[0], 0.75)
        colors[8] = lighten_color(colors[0], 0.25)
        colors[15] = colors[7]

    return colors
