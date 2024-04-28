# Functions related to file management
from tkinter import filedialog
from utils import print_to_terminal


# Function handles saving files
def save_file(data):
    """Function to save data as a text file."""
    # Prompt the user to select a file path for saving
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    # If a file path is provided by the user
    if file_path:
        # Write the text to the selected file and return message
        with open(file_path, "w") as f:  # File is closed after the with statement
            f.write(data)
        print_to_terminal("File saved")
    # Else return error
    else:
        print_to_terminal("File not saved")


# Function handles opening files
def open_file():
    """Function to open a file and return data"""
    # Prompt the user to select a file to open
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    # If a file path is provided by the user
    if file_path:
        # Open the selected file in read mode and return data then message
        with open(file_path, "r") as file:  # File is closed after the with statement
            data = file.read()
            print_to_terminal("File Opened")
            return data
    # Else returns null data and error
    else:
        data = None
        print_to_terminal("No file selected")
        return data

