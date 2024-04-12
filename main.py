# GUI constructor and Event Handler
import tkinter as tk
from tkinter import Menu, Text, Scrollbar
from file_handling import save_file, open_file  # Import file_handling functions for file operations
import command_parser


class GUI:
    def __init__(self):
        # Initialize the main Tkinter window
        self.root = tk.Tk()
        self.text_area = None  # Initialize text area attribute to None initially.
        self.terminal = None  # Initialize terminal attribute to None initially.
        self.gui_constructor()  # Call method to construct GUI components

    # Constructs the GUI window
    def gui_constructor(self):
        # Set window title
        self.root.title("Robot Programmer")

        # Create a text area widget for input
        self.text_area = Text(self.root, bg="black", fg="white")
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Create a menu bar
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        # Create a "File" dropdown menu inside menu bar
        file_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file_event)  # Add command to open file
        file_menu.add_command(label="Save", command=self.save_file_event)  # Add command to save file
        file_menu.add_separator()  # Separates options in the drop-down with a line
        file_menu.add_command(label="Run", command=self.run_file_event)

        # Create an "Edit" dropdown menu inside menu bar
        edit_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Text Area", command=self.clear_text_area)  # Add command to clear text area

        # Create a frame for the terminal output
        terminal_frame = tk.Frame(self.root)
        terminal_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Create a text widget for terminal output
        self.terminal = Text(terminal_frame, bg="black", fg="white", height=5)  # TODO: Colour text depending on error
        self.terminal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar for the terminal
        scrollbar = Scrollbar(terminal_frame, orient=tk.VERTICAL, command=self.terminal.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.terminal.config(yscrollcommand=scrollbar.set)

    # Handles all GUI events for opening a file
    def open_file_event(self):
        # Open file and display result in terminal
        data, terminal_message = open_file()  # Call function to open file...
        # ...function returns data and a message communicating success or error
        self.terminal.insert(tk.END, f"{terminal_message}\n")  # Display message in terminal
        if data:
            self.clear_text_area()  # Clear existing text in text area
            self.text_area.insert("1.0", data)  # Insert file contents in text area

    # Handles all GUI events for saving a file
    def save_file_event(self):
        # Save file and display result in terminal
        data = self.text_area.get("1.0", "end-1c")  # Get text from text area
        terminal_message = save_file(data)  # Call function to save file and pass text...
        # ... function returns a message communicating success or error
        self.terminal.insert(tk.END, f"{terminal_message}\n")  # Display message in terminal


    def run_file_event(self):
        data = self.text_area.get("1.0", "end-1c")  # Get text from text area
        terminal_message = command_parser.run_parser(data)  # Syntax check and tokenize, return terminal message
        self.terminal.insert(tk.END, f"{terminal_message}\n")  # Display message in terminal
        # Send Commands

    # Clears text area (seperated for readability)
    def clear_text_area(self):
        # Clear text area
        self.text_area.delete("1.0", "end")

    # Runs GUI event listener
    def run(self):
        # Run the main GUI loop
        self.root.mainloop()


if __name__ == "__main__":
    # Create GUI instance and run it
    gui = GUI()
    gui.run()
