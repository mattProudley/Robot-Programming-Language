#TODO: checksum

import time
#import serial
import struct
from utils import Result

serial_port = None


def _pack_data(tokens):
    packed_tokens = b''  # Initialize an empty byte stream

    # Iterate over tokens and pack each token into the byte stream
    for token, value in tokens:
        # Ensure value is an integer or None
        if value is None:
            value = 0  # Set default value to 0 for None

        # Pack token and value into bytes
        token_byte = bytes(token, 'utf-8')
        packed_tokens += struct.pack('cB', token_byte, value)
    return Result(packed_tokens, "Packed Data")


def _transmit_tokens(packed_data): # Serial Port
    # Send packed data over serial
    # serial_port.write(packed_data)
    return Result(packed_data, "Successfully Compiled and Sent")

def send(tokens):
    if tokens:
        result = _pack_data(tokens)
        result = _transmit_tokens(result.data)  # Serial Port
        _TEST_unpack_tokens(Result.data)
        return result


def _TEST_unpack_tokens(packed_tokens):
    return_tokens = []
    index = 0

    while index < len(packed_tokens):
        token_byte, value = struct.unpack_from('cB', packed_tokens, index)
        token = token_byte.decode('utf-8')
        return_tokens.append((token, value))
        index += struct.calcsize('cB')

    print("TEST unpacked tokens: ", return_tokens)

