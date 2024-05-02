# Handles bluetooth communication (currently set up for serial), handles sending/receiving and data packing/unpacking
import serial
import struct  # Struct library for packing and unpacking binary data
from utils import print_to_terminal
import time

# Global variable to store the serial port instance
serial_port = None


def setup_serial_port():
    # Sets up serial communication by opening a serial port connection
    global serial_port  # Declare serial_port as global to modify the variable
    try:
        print_to_terminal("Attempting to connect to serial")
        # Attempt to create a Serial object with the specified parameters
        serial_port = serial.Serial('COM8', 9600, timeout=1)  # Set port and baud rate
        # If successful, print confirmation to terminal
        print_to_terminal("Successfully connected to serial port")
        return True  # Return True to indicate success
    except serial.SerialException as e:
        # Handle exception if serial port connection fails
        print_to_terminal(f"Failed to open serial port: {e}, CHANGE PORT")
        serial_port = None  # Reset serial_port to None on error
        return False  # Return False to indicate failure


def check_serial_connection():
    global serial_port  # Use the global serial_port variable
    if serial_port is None:
        setup_serial_port()


def _pack_data_with_checksum(data):
    # Packs data and calculates checksum
    packed_data = b''  # Initialize an empty byte stream
    checksum = 0  # Initialize checksum to 0

    # Iterate over the data list, contains tuples of (token, value)
    for token, value in data:
        # If value is None (in the case of END; ), set it to 0 for consistency
        if value is None:
            value = 0
        # Convert token to bytes and pack token and value as bytes
        token_byte = bytes(token, 'utf-8')
        packed_data += struct.pack('c h', token_byte, value)
        print(packed_data)
        # Update checksum with token and value bytes
        checksum += token_byte[0] + value

    # Append checksum at the end of packed data, masking it to 8 bits
    checksum = checksum & 0xFF
    packed_data += struct.pack('B', checksum)
    # Print confirmation messages to the terminal
    print_to_terminal(f"Data packed {packed_data}")
    print_to_terminal(f"Checksum: {checksum}")
    return packed_data  # Return the packed data with appended checksum


def _ping_serial():
    global serial_port
    # Convert 'p' to bytes using encode()
    serial_port.write(b'p')  # Send the ping data over the serial port as bytes
    time.sleep(0.5)
    response = serial_port.read()  # Read the response from the serial port

    # Convert the response from bytes to string
    if response == b'p':
        print_to_terminal("Ping successful")
        return True
    else:
        print_to_terminal("Ping operation failed, data failed to send. Please check connection to robot")
        return False


def _transmit_data(packed_data):
    # Transmits packed data over the serial port
    global serial_port  # Use global serial_port variable
    if _ping_serial():
        serial_port.write(packed_data)  # Send the packed data over the serial port
        print_to_terminal("Successfully Sent")  # Print confirmation message to terminal


def send(data):
    # Sends data after packing it and adding a checksum
    if serial_port:
        if data:
            # Pack data and add checksum
            packed_data = _pack_data_with_checksum(data)
            # Transmit the packed data
            _transmit_data(packed_data)
            return packed_data  # Return the packed data (for debugging)
        else:
            # Print message if no data was provided to send
            print_to_terminal("No data passed to send function")
            return None  # Return None since no data was sent (for debugging)
    else:
        print_to_terminal("Error: No connection to robot. Reset program.")


def check_for_serial_data():
    # Checks for incoming data from the serial port
    if serial_port and serial_port.in_waiting > 0:
        # Read a line of incoming data from the serial port
        data = serial_port.readline().decode('utf-8').strip()
        # Print the received data to the terminal
        print_to_terminal(f"Robot: {data}")


def UNIT_TEST_unpack_data(packed_data):
    # Unpacks data for testing purposes
    return_tokens = []  # Initialize an empty list to hold the unpacked tokens and values
    index = 0  # Initialize index for iteration

    # Iterate through the packed data, unpacking each token-value pair
    while index < (len(packed_data) - 1):
        # Unpack token and value from the packed data
        token_byte, value = struct.unpack_from('c h', packed_data, index)
        token = token_byte.decode('utf-8')
        # Add the unpacked token and value to the list
        return_tokens.append((token, value))
        # Increment index by the size of the unpacked data
        index += struct.calcsize('c h')

    # Print unpacked tokens and values to the terminal for testing
    print_to_terminal(f"TEST unpacked tokens W/O checksum: {return_tokens}")

