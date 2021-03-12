import binascii
import struct

import pygatt

MAC = "BE:FF:20:00:FE:37"
CHAR = "0x0011"

adapter = pygatt.GATTToolBackend()
adapter.start()

device = adapter.connect(MAC, 15)

for uuid in device.discover_characteristics().keys():
    print("Read UUID %s: %s" % (uuid, binascii.hexlify(device.char_read(uuid))))
    print(device.char_read(uuid))


def getByteArray(message):
    data = []
    for x in message:
        if x < 0:
            data.append(int.from_bytes(struct.pack("!i", x), byteorder='little', signed=True))
        else:
            data.append(int.from_bytes(struct.pack("i", x), byteorder='little', signed=True))
    return data


print(getByteArray([126, 4, 4, 0, 0, 0, -1, 0, -17]))

# cmd = 'char-write-cmd 0x0100 {0}'.format(
#    ''.join("{0:02x}".format(byte) for byte in getByteArray([126, 4, 4, 0, 0, 0, -1, 0, -17]))
# )

# device.char_write("0000fff3-0000-1000-8000-00805f9b34fb", )
print()
print(device.char_read("0000fff3-0000-1000-8000-00805f9b34fb"))
# char-write-req 0x0008 7e000503ff000000ef
char = int("0xff", 16)
device.char_write("0000fff3-0000-1000-8000-00805f9b34fb", [0x7e, 0x00, 0x05, 0x03, 0x00, char, 0x00, 0x00, 0xef], wait_for_response=False)
print(device.char_read("0000fff3-0000-1000-8000-00805f9b34fb"))
# print(bytearray([0xFF0000]).decode("utf-8"))
# getByteArray("FF0000")
# bytearray(b'\x46\x46\x30\x30\x30\x30')

# 50 31 30 2d 43 5a 47 2d 56 35 2e 31 32 52 32 36 36 30 00 => (12, 255, 0)
# 7e 07 83 13 0d 08 02 ff ef 35 2e 31 32 52 32 36 36 30 00 => (0, 255, 247)
#  (255, 10, 0)
