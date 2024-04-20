# Preforms syntax checks and tokenizes batch files and commands
import re
from utils import Result

# Patterns and matching tokens used for tokenization process

# Tokens must be CHARS
token_map = {
    'MOV': 'F',
    'TURNL': 'L',
    'TURNR': 'R',
    'STOP': 'S',
    'FOR': 'f',
    # 'IF': 'i',
    'END': 'e',
    # 'READ': 'r'
}

def _compile_patterns():
    patterns = [
        r'MOV\s+([-+]?[1-9]\d*)',  # MOV command (+ forward, - reverse, cannot be 0)
        r'TURNL\s+([1-9][0-9]{0,2}|360)',  # TURN LEFT command (degrees, limited between 1 and 360)
        r'TURNR\s+([1-9][0-9]{0,2}|360)',  # TURN RIGHT command (degrees, limited between 1 and 360)
        r'STOP\s+([1-9]\d*)',  # STOP command (per seconds, cannot be 0)
        r'FOR\s+([1-9]\d+)',  # FOR loop command (iterative count, cannot be 0)
        # r'IF',
        r'END',
        # r'READ'
    ]

    compiled_patterns = [re.compile(pattern) for pattern in patterns]

    return compiled_patterns

def _validate_turnl(value_str)
        if not value_str
            return "Error: {command} is missing a value)"
        value = int(value_str)
        if not (1 <= value <= 360):
            return f"Error: Value is out of range or is a decimal number, (1-360) degrees"
        return None


def _split_commands(data_file):
    # If no data file
    if not data_file:
        return Result(False, "Error: No Data File Provided")

    # Remove trailing whitespaces, newlines, and null characters
    data = data_file.strip().replace('\n', '').replace('\0', '')

    # Find the index of the last complete statement terminator (;)
    last_semicolon_index = data.rfind(';')

    if last_semicolon_index == -1:
        return Result(False, "Syntax Error: No appropriate commands provided for syntax check.\n"
                             "Note: Single commands must still include a ';' e.g. 'MOV 10;'")

    # Check if the last statement is complete
    if last_semicolon_index != len(data) - 1:
        return Result(False, "Syntax Error: File ends unexpectedly.\n"
                             "Note: All commands must end with a ';' e.g. 'MOV 90;'")

    # Split statements by semicolon
    statements = data.split(';')

    # Remove any leftover whitespace created from split
    clean_data = [statement.strip() for statement in statements if statement.strip()]

    return Result(clean_data, "Data Cleaned")


def _pattern_match(patterns, commands):
    # Initialize an empty list to store matched commands
    matched_data = []

    # Iterate through each command in the provided list of commands
    for command in commands:
        # Initialize a boolean flag to indicate if the command is matched
        matched = False

        # Iterate through each pattern in the predefined patterns list
        for pattern in patterns:
            # Use regular expression to check if the command matches the current pattern
            if re.match(pattern, command):
                # If a match is found, append the command to the matched_data list
                matched_data.append(command)
                # Set the matched flag to True
                matched = True
                # Exit the inner loop since a match is found for the current command
                break

        # If no match is found for the current command, return a Result object indicating failure
        if not matched:
            return Result(False, f"Syntax Error: Unrecognized command '{command}'")

    # Return a Result object indicating success and the list of matched commands
    return Result(matched_data, "Pattern Matched")


def _tokenize(_pattern_matched_data):
    tokens = []  # Initialize an empty list to store tokens

    # Iterate through each command in the pattern-matched data
    for command in _pattern_matched_data:
        # Iterate through each pattern and its corresponding token in the token_map dictionary
        for pattern, token in token_map.items():
            # Check if the current command starts with the current pattern
            if command.startswith(pattern):
                # Use regular expression to check for a full match of the pattern in the command
                match = re.fullmatch(pattern + r'(\s+(\d+))?', command)
                if match:
                    # Extract the value from the command if present, otherwise default to 0
                    value = int(match.group(2)) if match.group(2) else 0
                    # Append the token and its corresponding value (if any) to the tokens list
                    tokens.append((token, value))
                    break  # Exit the inner loop once a match is found

    # Return a Result object containing the generated tokens and a success message
    return Result(tokens, "Tokenized")


def run_parser(data_file):
    if data_file:
        result = _split_commands(data_file)  # Clean the data file by removing whitespaces and unnecessary characters

        # Check if the data cleaning was successful
        if result.data:
            patterns = _compile_patterns()
            result = _pattern_match(patterns, result.data)  # Match the cleaned data file against predefined patterns

            # Check if the pattern matching was successful
            if result.data:
                result = _tokenize(result.data)  # Tokenize the pattern-matched data

        return result  # Return the final result containing the tokens or an error message
    return Result(False, "Error: No data file given to parse.")

    #def _check_block(_tokenized_data):
        # for length of token array
        #     if array i == f #for
        #         i = i+ 1
        #         for i in array
        #             if array i == end
        #                 break
        #             if array i == for
        #                 return error(no end statment)
        #     if array i = end
        #         retrun error (end before refrence)
        # return success

