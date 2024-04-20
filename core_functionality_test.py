import command_parser
import bluetooth
from utils import Result


def TEST_open_file(file_path):
    with open(file_path, "w") as f:  # File is closed after the with statement
        data = f.read()
    return Result(data, "File saved")


result = TEST_open_file(test_file)
result = command_parser.run_parser(result.data)
result = bluetooth.send(result.data)
