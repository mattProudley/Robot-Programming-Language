#TODO: checksum

import time
import serial
import struct
from utils import Result

serial_port = None


def send(tokens):
    packed_data = _pack_tokens(tokens)
    result = _transmit_tokens(packed_data) #Serial Port
    return result


def _pack_tokens(tokens):
    packed_tokens = b''  # Initialize an empty byte stream

    # Iterate over tokens and pack each token into the byte stream
    for token, value in tokens:
        # Ensure value is an integer or None
        if value is None:
            value = 0  # Set default value to 0 for None

        # Pack token and value into bytes
        token_byte = bytes(token, 'utf-8')
        packed_tokens += struct.pack('cB', token_byte, value)
    return packed_tokens


def _transmit_tokens(packed_data): # Serial Port
    print("Packed Tokens: ", packed_data)
    _TEST_unpack_tokens(packed_data)
    return Result(packed_data, "Successfully Sent")
    # Send packed data over serial
    # serial_port.write(packed_data)


def _TEST_unpack_tokens(packed_tokens):
    return_tokens = []
    index = 0

    while index < len(packed_tokens):
        token_byte, value = struct.unpack_from('cB', packed_tokens, index)
        token = token_byte.decode('utf-8')
        return_tokens.append((token, value))
        index += struct.calcsize('cB')

    print("TEST unpacked tokens: ", return_tokens)

