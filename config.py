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
