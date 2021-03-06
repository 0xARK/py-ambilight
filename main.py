#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          :
# Author             :
# Date created       :
# Date last modified :
# Python Version     : 3.*

import pyambilight

import argparse
import logging
import os
import sys

def get_args():
    """Get the script arguments."""
    description = "pyambi - synchronises rgb leds with your screen"
    arg = argparse.ArgumentParser(description=description)

    #arg.add_argument("-i", "--install", action="store_true",
    #                 help="Install all necessary dependencies on your platform. Use this command before run \
    #                      pyambi for the first time.")

    arg.add_argument("-q", "--quiet", action="store_true",
                     help="Quiet mode, hide all debug information.")

    arg.add_argument("-r", "--run", action="store_true",
                     help="Run pyambi in default mode (bluetooth). Only bluetooth mode is supported at this moment.")

    arg.add_argument("-t", "--test", action="store_true",
                     help="Run test with actual configuration for fps performance.")

    arg.add_argument("-v", "--version", action="store_true",
                     help="Print pyambi version.")

    return arg


def parse_args_exit(parser):
    """Process args that exit."""
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.version:
        parser.exit(0, "pyambi %s\n" % __version__)

    if args.test:
        pyambilight.tests.run_tests()
        sys.exit(0)

    if args.quiet:
        logging.getLogger().disabled = True
        sys.stdout = sys.stderr = open(os.devnull, "w")

    if args.install:
        pyambilight.dependencies.setup()
        sys.exit(0)


def parse_args(parser):
    """Process args."""
    args = parser.parse_args()

    if args.quiet:
        logging.getLogger().disabled = True
        sys.stdout = sys.stderr = open(os.devnull, "w")

    if args.run:
        pyambilight.stream.stream()


def main():
    """Main script function."""
    logging.basicConfig(format=("[%(levelname)s\x1b[0m] "
                                "\x1b[1;31m%(module)s\x1b[0m: "
                                "%(message)s"),
                        level=logging.INFO,
                        stream=sys.stdout)
    logging.addLevelName(logging.ERROR, '\x1b[1;31mE')
    logging.addLevelName(logging.INFO, '\x1b[1;32mI')
    logging.addLevelName(logging.WARNING, '\x1b[1;33mW')

    parser = get_args()

    parse_args_exit(parser)
    parse_args(parser)


if __name__ == "__main__":
    main()
