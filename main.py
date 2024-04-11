# Main file constructs the GUI and is responsible for handling GUI events.
import tkinter as tk
from tkinter import Menu, Scrollbar
from file_handling import save_file, open_file

text_area = None #TODO: variable not properly declared
terminal = None


# Function  called to create the GUI
def create_gui():
    global text_area, terminal

    # Create the main window
    root = tk.Tk()
    root.title("Robot Programmer")

    # Create a text area widget for input
    text_area = tk.Text(root, bg="black", fg="white")
    text_area.pack(fill=tk.BOTH, expand=True)

    # Create a menu bar
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    # Create a "File" dropdown menu inside menu bar
    file_menu = Menu(menu_bar, tearoff=False)
    # Add labels for functions
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open", command=open_file_command)
    file_menu.add_command(label="Save", command=save_file_command)
    file_menu.add_separator()
    file_menu.add_command(label="Run")

    # Create a frame for the terminal output
    terminal_frame = tk.Frame(root)
    terminal_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    # Create a text widget for terminal output
    terminal = tk.Text(terminal_frame, bg="black", fg="green", height=5)
    terminal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # Create a scrollbar for the terminal
    scrollbar = Scrollbar(terminal_frame, orient=tk.VERTICAL, command=terminal.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    terminal.config(yscrollcommand=scrollbar.set)\

    # Run the GUI
    root.mainloop()\



# Function to handle the "Open" menu command
def open_file_command():
    open_file(text_area)
    terminal.insert(tk.END, "File opened\n") # TODO: make this a global function and allow text colour control / also file opens message displays even if no file


# Function to handle the "Save" menu command
def save_file_command():
    save_file(text_area)
    terminal.insert(tk.END, "File saved\n")


# Main function
def main():
    create_gui()


if __name__ == "__main__":
    main()
