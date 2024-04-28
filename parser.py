# Preforms syntax checks and tokenizes batch files and commands
import re
from utils import print_to_terminal


# TODO: Quite a busy function, needs reformatting
def _clean_split_file(data_file):
    # Return None and print an error if no data file is provided
    if not data_file:
        # If errors return any errors and terminate further validation
        print_to_terminal("Error: No data file provided")
        return None

    # Remove unnecessary characters (whitespace, newlines, nulls) from the data file
    data = data_file.strip().replace('\n', '').replace('\0', '')

    # Identify the index of the last semicolon (statement terminator)
    last_semicolon_index = data.rfind(';')
    if last_semicolon_index == -1:
        # If errors return any errors and terminate further validation
        print_to_terminal("Syntax Error: No valid commands provided for syntax check.")
        return None

    # If the file doesn't end with a semicolon, print an error and return None
    if last_semicolon_index != len(data) - 1:
        # If errors return any errors and terminate further validation
        print_to_terminal("Syntax Error: File ends unexpectedly.")
        return None

    # Split data into individual statements by semicolon
    statements = data.split(';')

    # Strip whitespace and filter out empty statements
    clean_data = [statement.strip() for statement in statements if statement.strip()]

    # Log that the data file was cleaned and commands split
    print_to_terminal("Data file cleaned, commands split")
    return clean_data


def _compile_patterns():
    # Define a list of patterns (regular expressions) for different commands
    # Allows various types of numeric values or decimals through to validate later for better error messaging
    patterns = [
        # MOV command (may or may not include an integer or decimal value)
        r'MOV(?:\s+([-+]?\d+(\.\d+)?))?',
        # TURN LEFT command (may or may not include an integer or decimal value)
        r'TURNL(?:\s+([-+]?\d+(\.\d+)?))?',
        # TURN RIGHT command (may or may not include an integer or decimal value)
        r'TURNR(?:\s+([-+]?\d+(\.\d+)?))?',
        # STOP command (may or may not include an integer or decimal value)
        r'STOP(?:\s+([-+]?\d+(\.\d+)?))?',
        # FOR loop command (may or may not include an integer or decimal value)
        r'FOR(?:\s+([-+]?\d+))?',
        # END command (no additional value)
        r'END'
    ]

    # Compile each pattern using regular expressions and return the list of compiled patterns
    _compiled_patterns = [re.compile(pattern) for pattern in patterns]
    return _compiled_patterns


def _pattern_match(_compiled_patterns, clean_data):
    # Validators to confirm the correctness of command values
    validators = {
        'MOV': validate_mov,
        'TURNL': validate_turn,
        'TURNR': validate_turn,
        'STOP': validate_stop,
        'FOR': validate_for,
        # END command does not require validation
    }

    # List to store commands that match patterns
    matched_data = []

    # Iterate over each segment provided
    for segment in clean_data:
        matched = False  # Flag to indicate if the command was matched

        # Try each compiled pattern to see if it matches the command
        for pattern in _compiled_patterns:
            # Check if the command matches the pattern exactly
            match = pattern.fullmatch(segment)
            if match:
                # Extract command name and value if the pattern matches
                command = segment # Variable name change for clarity
                cmd_name = re.sub(r'[^A-Z]', '', pattern.pattern)

                # Validate the command value (if required)
                if cmd_name != 'END':
                    try:
                        validators[cmd_name](match.group(1))
                    except ValueError as e:
                        # If errors return any errors and terminate further validation
                        print_to_terminal(f"Syntax Error: {str(e)} in command '{command}'")
                        return None

                # Add the matched command to the list
                matched_data.append(command)
                matched = True  # Command has been matched
                break  # Exit loop since the command was matched

        # If no pattern matches, print an error and return None
        if not matched:
            # If errors return any errors and terminate further validation
            print_to_terminal(f"Syntax Error: Unrecognized command '{segment}'")
            return None

    # Log successful pattern matching
    print_to_terminal(f"Pattern Matched: {matched_data}")
    return matched_data


def validate_turn(value_str):
    if not value_str:
        raise ValueError("TURN command is missing a degrees value.")
    try:
        # Convert value string to integer
        value = int(value_str)
    except ValueError:
        raise ValueError(f"Invalid TURN value '{value_str}'. Expected an integer.")
    # Check value range
    if not (1 <= value <= 360):
        raise ValueError(f"TURN value {value} out of range (1-360).")
    return None


def validate_mov(value_str):
    if not value_str:
        raise ValueError("MOV command is missing a steps value.")
    try:
        value = int(value_str)  # Convert value string to integer
    except ValueError:
        raise ValueError(f"Invalid MOV value '{value_str}'. Expected an integer.")
    # Check range of MOV value
    if value == 0:
        raise ValueError("MOV value cannot be zero.")
    if value > 100:
        raise ValueError("MOV value too large. Must be less than 100.")
    if value < -100:
        raise ValueError("MOV value too small. Must be greater than -100.")
    return None


def validate_stop(value_str):
    if not value_str:
        raise ValueError("STOP command is missing a seconds value.")
    try:
        value = int(value_str)  # Convert value string to integer
    except ValueError:
        raise ValueError(f"Invalid STOP value '{value_str}'. Expected an integer.")
    # Check range of STOP value
    if value <= 0:
        raise ValueError(f"STOP value {value} must be greater than zero.")
    if not (1 <= value <= 60):
        raise ValueError(f"STOP value {value} out of range (1-60).")
    return None


def validate_for(value_str):
    if not value_str:
        raise ValueError("FOR command is missing a value.")
    try:
        value = int(value_str)  # Convert value string to integer
    except ValueError:
        raise ValueError(f"Invalid FOR value '{value_str}'. Expected an integer.")
    # Check range of FOR value
    if not (1 <= value <= 100):
        raise ValueError(f"FOR value {value} out of range (1-100).")
    return None


def _tokenize(verified_commands):
    # Mapping of command types to single-character tokens
    token_map = {
        'MOV': 'M',
        'TURNL': 'L',
        'TURNR': 'R',
        'STOP': 'S',
        'FOR': 'f',
        'END': 'e'
    }

    tokens = []  # List to store tokens

    # Iterate over each command in pattern-matched data
    for command in verified_commands:
        # Iterate over each pattern and its corresponding token
        for pattern, token in token_map.items():
            # Check if the command starts with the pattern
            if command.startswith(pattern):
                # Validate the command and extract the value
                match = re.fullmatch(pattern + r'(\s+(\d+))?', command)
                if match:
                    # Extract the integer value, defaulting to 0 if absent
                    value = int(match.group(2)) if match.group(2) else 0
                    # Append the token and value as a tuple to the tokens list
                    tokens.append((token, value))
                    break  # Exit loop after successful match
                else:
                    # Should never be reached but here incase
                    print_to_terminal("Error: Tokenizer exception")
                    return None

    # Log successful tokenization
    print_to_terminal(f"Tokenized: {tokens}")
    return tokens


def _check_blocks(tokens):
    block_stack = []  # Stack to track open blocks
    blocks = 0  # Counter for valid blocks
    f_count = 0  # Counter for consecutive 'f' (FOR) tokens

    # Iterate over each token in the tokenized data
    for i, (token, _) in enumerate(tokens):
        if token == 'f':
            # Increment FOR block stack and counter
            block_stack.append(token)
            f_count += 1

            # More than one FOR statement before an END is an error
            if f_count >= 2:
                print_to_terminal("Syntax Error: More than one FOR statement found before an END")
                return None

        elif token == 'e':
            # If an END token is found, check the block stack
            if block_stack:
                # Pop the top item from the block stack
                stack_top = block_stack.pop()
                # Reset FOR counter
                f_count = 0

                # Ensure the stack top matches a FOR token
                if stack_top != 'f':
                    print_to_terminal("Syntax Error: Unexpected END statement")
                    return None
                else:
                    blocks += 1  # Valid block found
            else:
                # Unmatched END token found
                print_to_terminal("Syntax Error: END statement before FOR loop reference")
                return None

    # Ensure no unmatched FOR statements remain in the stack
    if block_stack:
        print_to_terminal("Syntax Error: FOR statement missing an END statement")
        return None

    # If the loop completes without errors, the blocks are balanced
    print_to_terminal(f"Blocks checked, found {blocks} block/s")
    return tokens


def run_parser(data_file):
    # Parse the data file if provided
    if data_file:
        # Clean and split the data file into commands
        clean_data = _clean_split_file(data_file)

        # If successful, continue with further processing
        if clean_data:
            # Compile regular expression patterns
            patterns = _compile_patterns()
            # Match cleaned data against the patterns
            verified_commands = _pattern_match(patterns, clean_data)

            # If pattern matching is successful, proceed with tokenization
            if verified_commands:
                # Tokenize the verified commands
                tokens = _tokenize(verified_commands)

                # If tokenization is successful, check for balanced blocks
                if tokens:
                    final_data = _check_blocks(tokens)

                    # Return final compiled data if successful
                    if final_data:
                        return final_data
    else:
        # Print an error message if no data file is provided
        print_to_terminal("Error: No data file given to parse.")
    return None
