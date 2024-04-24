# Preforms syntax checks and tokenizes batch files and commands
import re
from utils import Result


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


def _compile_patterns():
    patterns = [
        r'MOV\s+([-+]?[1-9]\d*)',  # MOV command (+ forward, - reverse, cannot be 0)
        r'TURNL\s+([1-9][0-9]{0,2}|360)',  # TURN LEFT command (degrees, limited between 1 and 360)
        r'TURNR\s+([1-9][0-9]{0,2}|360)',  # TURN RIGHT command (degrees, limited between 1 and 360)
        r'STOP\s+([1-9]\d*)',  # STOP command (per seconds, cannot be 0)
        r'FOR\s+([1-9]\d+)',  # FOR loop command (iterative count, cannot be 0)
        r'END'
    ]
    _compiled_patterns = [re.compile(pattern) for pattern in patterns]
    return _compiled_patterns


def _pattern_match(_compiled_patterns, commands):
    # Initialize an empty list to store matched commands
    matched_data = []

    # Iterate through each command in the provided list of commands
    for command in commands:
        # Initialize a boolean flag to indicate if the command is matched
        matched = False

        # Iterate through each pattern in the predefined patterns list
        for pattern in _compiled_patterns:
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


def validate_turn(value_str):
    if not value_str:
        return "Error: TURN command is missing a degrees value."
    value = int(value_str)
    if not (1 <= value <= 360):
        return f"Error: TURN value {value} out of range (1-360)."
    return None


def validate_mov(value_str):
    if not value_str:
        return "Error: mov command is missing a steps value."
    value = int(value_str)
    if value == 0:
        return f"Error: mov value cannot be zero."
    return None


def validate_stop(value_str):
    if not value_str:
        return "Error: stop command is missing a seconds value."
    value = int(value_str)
    if value <= 0:
        return f"Error: stop value {value} must be greater than zero."
    return None


def _tokenize(_pattern_matched_data):
    # Tokens must be CHARS
    token_map = {
        'MOV': 'F',
        'TURNL': 'L',
        'TURNR': 'R',
        'STOP': 'S',
        'FOR': 'f',
        'END': 'e'
    }

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


def _check_blocks(_tokenized_data):
    block_stack = []

    for i, (token, _) in enumerate(_tokenized_data):
        if token == 'f':
            # Add 'for' to the stack to track the block
            block_stack.append(token)
        elif token == 'e':
            if block_stack:
                # If we encounter an 'end', check the stack
                stack_top = block_stack.pop()
                if stack_top != 'f':
                    return Result(False,  "Error: Unexpected 'end'")
            else:
                # If the stack is empty, this 'end' is unmatched
                return Result(False, "Error: 'end' before reference")

    if block_stack:
        # If the stack is not empty, there are unmatched statements
        return Result(False, "Error: No 'end' statement for 'for' at index")

    # If the loop completes without errors, the blocks are balanced
    return Result(_tokenized_data, "Blocks Checked")


def run_parser(data_file):
    if data_file:
        result = _split_commands(data_file)  # Clean the data file by removing whitespaces and unnecessary characters

        # Check if the data cleaning was successful
        if result.data:
            patterns = _compile_patterns()
            result = _pattern_match(patterns, result.data)  # Match the cleaned data file against predefined patterns

            # Check if the pattern matching was successful
            if result.data:
                result = _tokenize(result.data)  # Tokenize the pattern-matched data\

                # Check if tokenization was successful
                if result.data:
                    result = _check_blocks(result.data)  # Check all statement blocks are closed

        return result  # Return the final result containing the tokens or an error message

    return Result(False, "Error: No data file given to parse.")


