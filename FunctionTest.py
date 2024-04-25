import command_parser
import bluetooth
from file_handling import open_file
import time

bluetooth.setup_serial_port()
result = open_file()
result = command_parser.run_parser(result.data)
result = bluetooth.send(result.data)
while True:
    bluetooth.check_for_serial_data()
    time.sleep(1)
