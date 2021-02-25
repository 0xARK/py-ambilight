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
import subprocess
import colorsys
import sys

from const import RUN_PYAMBI


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


def saturate_colors(colors, amount):
    """Saturate all colors."""
    if amount and float(amount) <= 1.0:
        for i, _ in enumerate(colors):
            if i not in [0, 7, 8, 15]:
                colors[i] = saturate_color(colors[i], float(amount))

    return colors


def gen_colors(img):
    """Generate a colorscheme using Colorz."""
    # cmd = ["./lib/bin/schemer2", "-format", "img::colors", "-minBright", "0", "-in"]
    cmd = ["./lib/bin/schemer2", "-format", "img::colors", "-in"]
    colors = subprocess.check_output([*cmd, img]).splitlines()
    return colors


def adjust(cols, light):
    """Create palette."""
    # TODO: fix alt + tab bug
    res = ['#000000'] * 16

    if 'Could not get colors from image with settings specified. Aborting.' in cols[0]:
        res = ['#ffffff'] * 16
    else:
        try:
            cols.sort(key=rgb_to_yiq)
            raw_colors = [*cols[8:], *cols[8:]]
            res = generic_adjust(raw_colors, light)
        except:
            pass

    return res


# TODO : schemer2 detection and installation
def get(img, light=False, sat=""):
    """Get colorscheme."""
    if not os.path.isfile("./lib/bin/schemer2"):
        logging.error("Required dependencies don't seem to be installed. " +
                      "Please run '" + RUN_PYAMBI + " -i' to install it.")
        sys.exit(1)

    cols = [col.decode('UTF-8') for col in gen_colors(img)]
    colors = adjust(cols, light)
    return saturate_colors(colors, sat)[1:4]


def get_lightest(rgb):
    """Get lightest color."""
    last_lightest = 0
    index = 0

    for i in range(len(rgb)):
        indice = rgb[i][0] + rgb[i][1] + rgb[i][2]
        if indice > last_lightest:
            last_lightest = indice
            index = i

    return rgb[index], rgb_to_hex(rgb[index])


def hex_to_rgb(color):
    """Convert a hex color to rgb."""
    return tuple(bytes.fromhex(color.strip("#")))


def rgb_to_hex(color):
    """Convert an rgb color to hex."""
    return "#%02x%02x%02x" % (*color,)


def rgb_to_yiq(color):
    """Sort a list of colors."""
    return colorsys.rgb_to_yiq(*hex_to_rgb(color))


def darken_color(color, amount):
    """Darken a hex color."""
    color = [int(col * (1 - amount)) for col in hex_to_rgb(color)]
    return rgb_to_hex(color)


def lighten_color(color, amount):
    """Lighten a hex color."""
    color = [int(col + (255 - col) * amount) for col in hex_to_rgb(color)]
    return rgb_to_hex(color)


def saturate_color(color, amount):
    """Saturate a hex color."""
    r, g, b = hex_to_rgb(color)
    r, g, b = [x / 255.0 for x in (r, g, b)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s = amount
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    r, g, b = [x * 255.0 for x in (r, g, b)]

    return rgb_to_hex((int(r), int(g), int(b)))


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
