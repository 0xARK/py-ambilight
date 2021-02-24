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

import platform

# screen width in pixel
swidth = 1920
# screen height in pixel
sheight = 1080

# resize base for resize image captured and analyse it after
# high value = low performance but high color fidelity
# low value = high performance but we lose a little bit in colour fidelity
# recommended value for FHD screen (1920x1080) : 150
# highest recommended value for FHD screen (1920x1080) : 500
# lowest recommended value for FHD screen (1920x1080) : 25
resize_base = 50

# monitor to capture
dimension_screen = {'top': 150, 'left': 100, 'width': 1820, 'height': 930}
current_screen = False


# current version of pyambi
__version__ = "0.5.0"

# current os platform (Linux, Darwin or Windows)
OS = platform.uname()[0]

# Go version required for schemer2
GO_VERSION_REQUIRED = "go1.15.8"

# Go download url for each platform
GO_LINUX_DOWNLOAD_URL = "https://golang.org/dl/" + GO_VERSION_REQUIRED + ".linux-amd64.tar.gz"
GO_DARWIN_DOWNLOAD_URL = "https://golang.org/dl/" + GO_VERSION_REQUIRED + ".darwin-amd64.pkg"
GO_WINDOWS_DOWNLOAD_URL = "https://golang.org/dl/" + GO_VERSION_REQUIRED + ".windows-amd64.msi"

# Schemer2 repository information
GITHUB_URL = "github.com"
GITHUB_USER = "thefryscorer"
GITHUB_PROJECT = "schemer2"

# basic command for run pyambi project
RUN_PYAMBI = "python3 pyambi.py"

# pip required dependencies
PIP_DEPENDENCIES = ["opencv-python", "argparse", "urllib3", "numpy", "mss", "Pillow"]
