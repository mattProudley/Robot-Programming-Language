import serial
import struct
from utils import print_to_terminal

serial_port = None


def setup_serial_port():
    global serial_port
    # Set up serial communication with the specified port and baud rate
    try:
        serial_port = serial.Serial('COM6', 9600, timeout=1) # CHECK COM PORT BEFORE RUNNING
        print_to_terminal("Successfully connected to serial port")
        return True
    except serial.SerialException as e:
        print_to_terminal(f"Failed to open serial port: {e}, CHANGE PORT")
        serial_port = None  # Set to None if there is an error
        return False


# Functions for sending data
def _pack_data_with_checksum(data):
    packed_data = b''  # Initialize an empty byte stream
    # Calculate checksum
    checksum = 0

    # Iterate over tokens and pack each token into the byte stream
    for token, value in data:
        # Ensure value is an integer or None
        if value is None:
            value = 0  # Set default value to 0 for None

        # Pack token and value into bytes
        token_byte = bytes(token, 'utf-8')
        packed_data += struct.pack('cB', token_byte, value)
        # Update checksum
        checksum += token_byte[0] + value

    # Append checksum at the end of data
    # checksum = checksum + 1 # Test checksum algorithm
    packed_data += struct.pack('B', checksum & 0xFF)  # Mask checksum to 8 bits

    # Return packed data
    print_to_terminal("Data packed")
    print_to_terminal(f"Checksum: {checksum}")
    return packed_data


def _transmit_data(packed_data): # Serial Port
    # Send packed data over serial
    global serial_port
    serial_port.write(packed_data)
    print_to_terminal("Successfully Sent")


def send(data):
    if data:
        packed_data = _pack_data_with_checksum(data)
        _transmit_data(packed_data)  # Serial Port
        return packed_data
    else:
        print_to_terminal("No data passed to send function")
        return None


def check_for_serial_data():
    if serial_port and serial_port.in_waiting > 0:
        data = serial_port.readline().decode('utf-8').strip()
        print_to_terminal(f"Robot: {data}")


def UNIT_TEST_unpack_data(packed_data):
    return_tokens = []
    index = 0

    while index < (len(packed_data) -1):
        token_byte, value = struct.unpack_from('cB', packed_data, index)
        token = token_byte.decode('utf-8')
        return_tokens.append((token, value))
        index += struct.calcsize('cB')

    print_to_terminal(f"TEST unpacked tokens W/O checksum: {return_tokens}")

