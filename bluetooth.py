import serial
import struct
from utils import Result

serial_port = None


def setup_serial_port():
    global serial_port
    # Set up serial communication with the specified port and baud rate
    try:
        serial_port = serial.Serial('COM6', 9600, timeout=1) # CHECK COM PORT BEFORE RUNNING
        print(serial_port)
    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}, CHANGE PORT")
        serial_port = None  # Set to None if there is an error


# Functions for sending data
def _pack_data_with_checksum(tokens):
    packed_tokens = b''  # Initialize an empty byte stream

    # Calculate checksum
    checksum = 0

    # Iterate over tokens and pack each token into the byte stream
    for token, value in tokens:
        # Ensure value is an integer or None
        if value is None:
            value = 0  # Set default value to 0 for None

        # Pack token and value into bytes
        token_byte = bytes(token, 'utf-8')
        packed_tokens += struct.pack('cB', token_byte, value)
        # Update checksum
        checksum += token_byte[0] + value

    # Append checksum at the end of data
    # checksum = checksum + 1 # Test checksum algorithm
    print("Checksum: ", checksum)
    packed_tokens += struct.pack('B', checksum & 0xFF)  # Mask checksum to 8 bits

    # Return packed data
    return Result(packed_tokens, "Packed Data")


def _send_packed_data(packed_data): # Serial Port
    # Send packed data over serial
    serial_port.write(packed_data)
    return Result(packed_data, "Successfully Compiled and Sent")


def send(data):
    if data:
        result = _pack_data_with_checksum(data)
        result = _send_packed_data(result.data)  # Serial Port
        return result
    else:
        return Result(False, "No data passed to send function")


# Functions for receiving data
def bluetooth_receive():
    # Check if there is data available on the serial port
    if serial_port.in_waiting > 0:
        try:
            # Read data from the serial port
            data = serial_port.readLine().strip()
            # Decode data from ASCII values to characters
            decoded_data = data.decode('utf-8')
            print(f"Received from Arduino: {decoded_data}")

        except UnicodeDecodeError as e:
            # Handle any decoding errors gracefully
            print(f"Error decoding data: {e}")


def check_for_serial_data():
    if serial_port and serial_port.in_waiting > 0:
        data = serial_port.readline().decode('utf-8').strip()
        print(f"Received from Arduino: {data}")


def UNIT_TEST_unpack_data(packed_tokens):
    return_tokens = []
    index = 0

    while index < (len(packed_tokens) -1):
        token_byte, value = struct.unpack_from('cB', packed_tokens, index)
        token = token_byte.decode('utf-8')
        return_tokens.append((token, value))
        index += struct.calcsize('cB')

    print("TEST unpacked tokens W/O checksum: ", return_tokens)

