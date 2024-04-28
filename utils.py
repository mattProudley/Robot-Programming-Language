import tkinter as tk

# A global variable to hold the terminal reference
terminal_reference = None


def set_terminal_reference(terminal):
    global terminal_reference
    terminal_reference = terminal


def print_to_terminal(message):
    # Access the global terminal reference
    global terminal_reference
    # Print the message to the program terminal
    if terminal_reference is not None:
        terminal_reference.insert(tk.END, f"{message}\n")
        terminal_reference.see(tk.END)
    # Print message to main IDE terminal
    print(message)


