import tkinter as tk

# A global variable to hold the terminal reference (Tkinter Text widget)
terminal_reference = None


def set_terminal_reference(terminal):
    # Assigns the provided Tkinter Text widget as the global terminal reference
    global terminal_reference
    terminal_reference = terminal


def print_to_terminal(message):
    # Prints the given message to the Tkinter Text widget (if set) and the IDE terminal
    global terminal_reference
    if terminal_reference:
        # Insert the message at the end of the Tkinter Text widget
        terminal_reference.insert(tk.END, f"{message}\n")
        # Scroll to make the new message visible
        terminal_reference.see(tk.END)
    # Print the message to the IDE terminal
    print(message)
