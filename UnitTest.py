# Tests core functionality of the program, opening a batch file, compiling, and bluetooth communication
import parser
import bluetooth
from file_handling import open_file
import time

# Define the timeout duration in seconds (e.g., 60 seconds)
timeout_duration = 20
# Initialize the start time
start_time = time.time()

if bluetooth.setup_serial_port(): # Setup serial port
    data = open_file() # Open / Select File
    if data:
        parsed_data = parser.run_parser(data) # Run token compiler
        if parsed_data:
            packed_data = bluetooth.send(parsed_data) # Pack and send data over bluetooth
            if packed_data:
                bluetooth.UNIT_TEST_unpack_data(packed_data) # Unpack data to ensure data is packed correctly

                # Check for response from arduino
                while True:
                    bluetooth.check_for_serial_data()  # Check for serial data
                    elapsed_time = time.time() - start_time  # Calculate the elapsed time since the loop started
                    # Break the loop if the elapsed time exceeds the timeout duration
                    if elapsed_time > timeout_duration:
                        print("Timeout reached. Exiting loop.")
                        break
                    time.sleep(0.5)  # Wait to slow terminal print
