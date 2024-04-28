# Tests core functionality of the program, opening a batch file, compiling, and bluetooth communication
import command_parser
import bluetooth
from file_handling import open_file
import time

# Define the timeout duration in seconds (e.g., 60 seconds)
timeout_duration = 20

# Initialize the start time
start_time = time.time()

bluetooth.setup_serial_port() # Setup serial port
result = open_file() # Open / Select File
result = command_parser.run_parser(result.data) # Run token compiler
result = bluetooth.send(result.data) # Pack and send data over bluetooth
bluetooth.UNIT_TEST_unpack_data(result.data) # Unpack data to ensure data is packed correctly

# Check for response from arduino
while True:
    bluetooth.check_for_serial_data()  # Check for serial data
    elapsed_time = time.time() - start_time  # Calculate the elapsed time since the loop started
    # Break the loop if the elapsed time exceeds the timeout duration
    if elapsed_time > timeout_duration:
        print("Timeout reached. Exiting loop.")
        break
    time.sleep(0.5)  # Wait to slow terminal print
