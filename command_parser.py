#TODO: commands without variables need a specific error message
#TODO: tokenization funciton can be optimised
# #TODO: loop or if does not end

# Preforms syntax checks and tokenizes batch files and commands
import re
from utils import Result

# Patterns and matching tokens used for tokenization process
patterns = [
    r'MOV\s+(\d+)',  # MOV command
    r'TURNL\s+(\d+)',  # TURN LEFT command
    r'TURNR\s+(\d+)',  # TURN RIGHT command
    r'STOP',  # STOP command (include per seconds)
    r'FOR\s+(\d+)',
    r'END',
    r'READ'
]

# Tokens must be CHARS
token_map = {
    'MOV': 'F',
    'TURNL': 'L',
    'TURNR': 'R',
    'STOP': 'S',
    'FOR': 'f',
    'END': 'e',
    'READ': 'r'
}


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

    print("Cleaned Data: ", clean_data)
    return Result(clean_data, "Data Cleaned")


def _pattern_match(commands):
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

    # Print the matched commands for debugging purposes
    print("Matched Data: ", matched_data)

    # Return a Result object indicating success and the list of matched commands
    return Result(matched_data, "Pattern Matched")


# def _check_loop_closed(pattern_matched_data):


def _tokenize(pattern_matched_data):
    tokens = []  # Initialize an empty list to store tokens

    # Iterate through each command in the pattern-matched data
    for command in pattern_matched_data:
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

        # Debugging: Print the generated tokens
    print("Tokens: ", tokens)

    # Return a Result object containing the generated tokens and a success message
    return Result(tokens, "Successfully Compiled")


def run_parser(data_file):
    result = _split_commands(data_file)  # Clean the data file by removing whitespaces and unnecessary characters

    # Check if the data cleaning was successful
    if result.data:
        result = _pattern_match(result.data)  # Match the cleaned data file against predefined patterns

        # Check if the pattern matching was successful
        if result.data:
            result = _check_loop_closed(result.data)  # Check if loops are properly closed

            # Check if the loop closure check was successful
            if result.data:
                result = _tokenize(result.data)  # Tokenize the pattern-matched data

    return result  # Return the final result containing the tokens or an error message

