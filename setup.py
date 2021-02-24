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
import sys
import urllib.request

import config


def install_go_linux(url):
    """Check for go language version on linux and install it."""

    logging.info("Version 1.15.8 of go language is required and will be installed locally.")
    logging.info("Download in progress, please wait.")

    if not os.path.isdir('./lib'):
        os.mkdir('lib')

    if os.path.isfile('./lib/go/bin/go'):

        logging.info(subprocess.check_output(['./lib/go/bin/go', 'version']).decode("utf-8").replace('\n', ''))
        logging.info("Go language version 1.15.8 has already been downloaded and installed.")

    elif os.path.isfile('./lib/go1.15.8.linux-amd64.tar.gz'):

        logging.info("The file has already been downloaded.")
        logging.info("Start installation.")
        subprocess.check_output(['tar', '-C', './lib', '-xzf',
                                 './lib/' + config.GO_VERSION_REQUIRED + '.linux-amd64.tar.gz'])
        logging.info(subprocess.check_output(['./lib/go/bin/go', 'version']).decode("utf-8").replace('\n', ''))
        logging.info("Installation of version 1.15.8 finished.")

    else:

        urllib.request.urlretrieve(url, './lib/go1.15.8.linux-amd64.tar.gz')
        logging.info("Download finished.")
        logging.info("Start installation.")
        subprocess.check_output(['tar', '-C', './lib', '-xzf',
                                 './lib/' + config.GO_VERSION_REQUIRED + '.linux-amd64.tar.gz'])
        logging.info(subprocess.check_output(['./lib/go/bin/go', 'version']).decode("utf-8").replace('\n', ''))
        logging.info("Installation of version 1.15.8 finished.")


def install_go_darwin(url):
    pass


def install_go_windows(url):
    pass


def install_go():
    """Install go locally on current OS."""

    # TODO : MacOS and Windows dependencies installation
    if config.OS == 'Linux':
        install_go_linux(config.GO_LINUX_DOWNLOAD_URL)
    # elif OS == 'Darwin':
    #     install_go_darwin(config.GO_DARWIN_DOWNLOAD_URL)
    # elif OS == "Windows":
    #     install_go_windows(config.GO_WINDOWS_DOWNLOAD_URL)
    else:
        logging.error("Sorry, this OS is not currently supported.")


def install_schemer2():
    """Clone schemer2 repository and build it."""
    logging.info("Schemer2 is required and will be installed locally.")
    logging.info("Download and installation in progress, please wait.")

    cwd = config.GITHUB_URL + '/' + config.GITHUB_USER + '/' + config.GITHUB_PROJECT

    if not os.path.isdir('./lib/src/' + cwd) and not os.path.isfile('./lib/bin/schemer2'):
        subprocess.check_output(['./lib/go/bin/go', 'get', cwd])
        logging.info("Download and installation finished")
    else:
        logging.info("The dependency has already been downloaded and installed.")


def install_pip_packages():
    """Install all required pip dependencies"""
    output = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in output.split()]

    for name in config.PIP_DEPENDENCIES:
        if name not in installed_packages:
            logging.warning("Pip package " + name + " may not be installed and is about to be reinstalled. Please wait.")
            subprocess.check_output([sys.executable, "-m", "pip", "install", name])
        else:
            logging.info("Pip package " + name + " has been found and will not be installed.")


def setup():
    """Install required dependencies"""
    if "GOROOT" in os.environ:
        goroot_backup = os.environ['GOROOT']
    else:
        goroot_backup = ""

    if "GOPATH" in os.environ:
        gopath_backup = os.environ['GOPATH']
    else:
        gopath_backup = ""

    os.environ['GOROOT'] = subprocess.check_output(['pwd']).decode("utf-8").replace('\n', '') + '/lib/go'
    os.environ['GOPATH'] = subprocess.check_output(['pwd']).decode("utf-8").replace('\n', '') + '/lib'

    print()
    logging.info("Installing dependency, step 1 of 3.\n")
    install_go()

    print()
    logging.info("Installing dependency, step 2 of 3.\n")
    install_schemer2()

    print()
    logging.info("Installing dependency, step 3 of 3.\n")
    install_pip_packages()

    if goroot_backup != "":
        os.environ['GOROOT'] = goroot_backup

    if gopath_backup != "":
        os.environ['GOPATH'] = gopath_backup
