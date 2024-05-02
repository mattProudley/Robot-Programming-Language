# Tests core functionality of the program, including file handling, compiling, and Bluetooth communication
import parser
import bluetooth
from file_handling import open_file
import time

# Define the timeout duration in seconds (e.g., 20 seconds)
timeout_duration = 60

# Store the start time of the operation
start_time = time.time()

# Check if the serial port is set up successfully for Bluetooth communication
if bluetooth.setup_serial_port():
    # Select and open a file, read the data
    data = open_file()
    if data:
        # Parse the data using the token compiler
        parsed_data = parser.run_parser(data)
        if parsed_data:
            # Pack and send the parsed data over Bluetooth
            packed_data = bluetooth.send(parsed_data)
            if packed_data:
                # Unpack the data to ensure the packing was successful
                bluetooth.UNIT_TEST_unpack_data(packed_data)

                # Continuously check for a response from the Arduino until timeout is reached
                while True:
                    # Check for any incoming serial data and print it
                    bluetooth.check_for_serial_data()
                    # Calculate the elapsed time since the loop began
                    elapsed_time = time.time() - start_time
                    # Exit the loop if the timeout duration is exceeded
                    if elapsed_time > timeout_duration:
                        print("Timeout reached. Exiting loop.")
                        break
                    # Pause briefly to avoid excessive terminal printing
                    time.sleep(0.5)
