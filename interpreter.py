
#TODO: text without a ; will be ignored or added to next command
#TODO: ensure all data varaibles are null after use
import re

# Patterns used for comparison, stored in an array for now,
# but will affect compilation times depending on number of supported commands
patterns = [
    r'MOV\s+(\d+)',  # MOV command
    r'TURNL\s+(\d+)',  # TURN LEFT command
    r'TURNR\s+(\d+)',  # TURN RIGHT command
    r'STOP',  # STOP command
]


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

# def tokenize(checked_data):
#     if checked_data:


def run_interpreter(data_file):
    if data_file:
        clean_data = clean(data_file)  # Data file is cleaned removing whitespaces and unnecessary characters
    if clean_data:
        print(clean_data) # DEBUGGING
        checked_data = syntax_check(clean_data)  # Returned data is checked against the syntax
    if checked_data:
        print(checked_data) # DEBUGGING
        tokenize(checked_data)
        print("Code 0")
#     generate_tokens(data)
#     print tokens

# def lex(data):
#     tokens = []
#
#     # Combine the patterns
#     combined_pattern = f'({mov_pattern})|({turn_pattern})'
#
#     # Tokenize the data
#     for match in re.finditer(combined_pattern, data):
#         if match.group(1):  # MOV command
#             tokens.append(('MOV', int(match.group(2))))
#         elif match.group(3):  # TURN command
#             tokens.append(('TURN', int(match.group(4))))
#
#     return tokens
#
#
# # Example usage
# data = 'MOV "10", TURN "20", MOV "30"'
# tokens = lexer(data)
# print(tokens)
