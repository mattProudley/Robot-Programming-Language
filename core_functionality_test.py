import command_parser
import bluetooth
from file_handling import open_file

result = open_file()
result = command_parser.run_parser(result.data)
result = bluetooth.send(result.data)
