#TODO: text without a ; will be ignored or added to next command
#TODO: ensure all data varaibles are null after use
#TODO: tokenization funciton can be optimised
#TODO: error messages in terminal

# Preforms syntax checks and tokenizes batch files and commands
import re

# Patterns and matching tokens used for tokenization process, stored in an 2D array (for now)
patterns = [
    r'MOV\s+(\d+)',  # MOV command
    r'TURNL\s+(\d+)',  # TURN LEFT command
    r'TURNR\s+(\d+)',  # TURN RIGHT command
    r'STOP',  # STOP command
]

token_map = {
    'MOV': 'M',
    'TURNL': 'TL',
    'TURNR': 'TR',
    'STOP': 'S',

}


def clean(data_file):
    if data_file:
        # Remove trailing whitespaces, newlines, and null characters
        data = data_file.strip().replace('\n', '').replace('\0', '')

        # Split lines by semicolon into a list
        # TODO: This won't support large files
        statements = data.split(';')

        # Remove any leftover whitespace
        clean_data = [statement.strip() for statement in statements]

        # Remove last blank statement resulting from split
        clean_data.pop()
        return clean_data


def syntax_check(clean_data):
    if clean_data:
        checked_data = []
        for command in clean_data:
            matched = False
            for pattern in patterns:
                if re.match(pattern, command):
                    checked_data.append(command)
                    matched = True
                    break
            if not matched:
                print("CODE 1: ", f"Syntax Error: {command}")
                checked_data = None
                break
        return checked_data


def tokenize(checked_data):
    tokens = []
    for command in checked_data:
        matched = False
        for pattern, token in token_map.items():
            if command.startswith(pattern):
                match = re.match(pattern + r'(\s+(\d+))?', command)
                if match:
                    matched = True
                    value = int(match.group(2)) if match.group(2) else None
                    tokens.append((token, value))
                    break  # Exit the loop once a match is found
        if not matched:
            print("CODE 1: ", f"Syntax Error: {command}")
            return None
    return tokens


def run_parser(data_file):
    if data_file:
        clean_data = clean(data_file)  # Data file is cleaned removing whitespaces and unnecessary characters
    if clean_data:
        print(clean_data) # DEBUGGING
        checked_data = syntax_check(clean_data)  # Cleaned data file is checked against the syntax
    if checked_data:
        print(checked_data) # DEBUGGING
        tokens = tokenize(checked_data)
    if tokens:
        print(tokens) # DEBUGGING
        terminal_message = "Passed"
    return terminal_message

