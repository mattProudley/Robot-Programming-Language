#TODO: ensure all data varaibles are null after use
#TODO: tokenization funciton can be optimised
#TODO: add more syntax error feeback
#TODO: commands without variables need a specific error message


# Preforms syntax checks and tokenizes batch files and commands
import re
from utils import Result

# Patterns and matching tokens used for tokenization process
patterns = [
    r'MOV\s+(\d+)',  # MOV command
    r'TURNL\s+(\d+)',  # TURN LEFT command
    r'TURNR\s+(\d+)',  # TURN RIGHT command
    r'STOP',  # STOP command
]

# Tokens must be CHARS
token_map = {
    'MOV': 'F',
    'TURNL': 'L',
    'TURNR': 'R',
    'STOP': 'S',
}


def _clean(data_file):
    # If no data file
    if not data_file:
        return Result(False, "Error: No Data File Provided")

    # Remove trailing whitespaces, newlines, and null characters
    data = data_file.strip().replace('\n', '').replace('\0', '')

    # Find the index of the last complete statement terminator (;)
    last_semicolon_index = data.rfind(';')

    if last_semicolon_index == -1:
        return Result(False, "Syntax Error: No appropriate commands provided for syntax check.")

    # Check if the last statement is complete
    if last_semicolon_index != len(data) - 1:
        return Result(False, "Syntax Error: File ends unexpectedly.")

    # Split statements by semicolon
    statements = data.split(';')

    # Remove any leftover whitespace created from split
    clean_data = [statement.strip() for statement in statements if statement.strip()]

    print("Cleaned Data: ", clean_data)
    return Result(clean_data, "Data Cleaned")


def _pattern_match(commands):
    matched_data = []
    for command in commands:
        matched = False
        for pattern in patterns:
            if re.match(pattern, command):
                matched_data.append(command)
                matched = True
                break
        if not matched:
            return Result(False, f"Syntax Error: Unrecognized command '{command}'")
    print("Matched Data: ", matched_data)
    return Result(matched_data, "Pattern Matched")


def _tokenize(pattern_matched_data):
    tokens = []
    for command in pattern_matched_data:
        matched = False
        for pattern, token in token_map.items():
            if command.startswith(pattern):
                match = re.fullmatch(pattern + r'(\s+(\d+))?', command)
                if match:
                    matched = True
                    value = int(match.group(2)) if match.group(2) else 0
                    tokens.append((token, value))
                    break  # Exit the loop once a match is found
    print("Tokens: ", tokens)  # DEBUGGING
    return Result(tokens, "Successfully Compiled")


def run_parser(data_file):
    result = _clean(data_file)  # Data file is cleaned removing whitespaces and unnecessary characters
    if result.data:
        result = _pattern_match(result.data)  # Cleaned data file is checked against the syntax
        if result.data:
            result = _tokenize(result.data)
    return result
