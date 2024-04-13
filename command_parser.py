#TODO: text without a ; will be ignored or added to next command
# trailing text at end of file allout
# charector simply pass??
#TODO: ensure all data varaibles are null after use
#TODO: tokenization funciton can be optimised
#TODO: add more syntax error feeback


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
    # Remove trailing whitespaces, newlines, and null characters
    data = data_file.strip().replace('\n', '').replace('\0', '')

    statements = data.split(';')

    # Remove any leftover whitespace
    clean_data = [statement.strip() for statement in statements]

    # Remove last blank statement resulting from split
    clean_data.pop()
    return clean_data


def _syntax_check(clean_data):
    checked_data = []
    for command in clean_data:
        matched = False
        for pattern in patterns:
            if re.match(pattern, command):
                checked_data.append(command)
                matched = True
                break
        if not matched:
            return Result(False, f"Syntax Error: Unrecognized command {command}")
    return Result(checked_data, "Passed Syntax Check")


def _tokenize(checked_data):
    tokens = []
    for command in checked_data:
        matched = False
        for pattern, token in token_map.items():
            if command.startswith(pattern):
                match = re.match(pattern + r'(\s+(\d+))?', command)
                if match:
                    matched = True
                    value = int(match.group(2)) if match.group(2) else 0
                    tokens.append((token, value))
                    break  # Exit the loop once a match is found
    return Result(tokens, "Successfully Compiled")


def run_parser(data_file):
    clean_data = _clean(data_file)  # Data file is cleaned removing whitespaces and unnecessary characters
    result = _syntax_check(clean_data)  # Cleaned data file is checked against the syntax
    if result.data:
        result = _tokenize(result.data)
        print("Tokens: ", result.data)  # DEBUGGING
    return result
