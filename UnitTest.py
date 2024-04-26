# Tests core functionality of the program, opening a batch file, compiling, and bluetooth communication
import command_parser
import bluetooth
from file_handling import open_file
import time

# Define the timeout duration in seconds (e.g., 60 seconds)
timeout_duration = 10

# Initialize the start time
start_time = time.time()

bluetooth.setup_serial_port()
result = open_file()
result = command_parser.run_parser(result.data)
result = bluetooth.send(result.data)
bluetooth.UNIT_TEST_unpack_data(result.data)

while True:
    # Check for serial data
    bluetooth.check_for_serial_data()

    # Calculate the elapsed time since the loop started
    elapsed_time = time.time() - start_time

    # Break the loop if the elapsed time exceeds the timeout duration
    if elapsed_time > timeout_duration:
        print("Timeout reached. Exiting loop.")
        break