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

def palette(rgb, background=False, legend=[]):
    """Generate a palette from the colors."""
    n = len(rgb)

    for i in range(0, n * 2):
        if i % n == 0:
            print()

        if legend:
            print("\033[%s8;2;%s;%s;%sm%s\033[0m" % (
                4 if background else 3, rgb[round(i % n)][0], rgb[round(i % n)][1], rgb[round(i % n)][2],
                " " * (80 // 20)),
                  end=" " + legend[i % n] + " ")
        else:
            print("\033[%s8;2;%s;%s;%sm%s\033[0m" % (
                4 if background else 3, rgb[round(i % n)][0], rgb[round(i % n)][1], rgb[round(i % n)][2],
                " " * (80 // 20)),
                  end=" ")

    print()
