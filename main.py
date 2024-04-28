# GUI constructor and Event Handler
import tkinter as tk
from tkinter import Menu, Text, Scrollbar
from file_handling import save_file, open_file  # Import file_handling functions for file operations
import parser
import bluetooth
from utils import set_terminal_reference


class GUI:
    def __init__(self):
        # Initialize the main Tkinter window
        self.root = tk.Tk()
        self.text_area = None  # Initialize text area attribute to None initially.
        self.terminal = None  # Initialize terminal attribute to None initially.
        self.gui_constructor()  # Call method to construct GUI components
        self.setup_bluetooth()  # Sets up serial port

    def setup_bluetooth(self):
        bluetooth.setup_serial_port()

    # Constructs the GUI window
    def gui_constructor(self):
        # Set window title
        self.root.title("Robot Programmer")

        # Set the default size of the window
        self.root.geometry("800x600")  # Set the width to 800 pixels and height to 600 pixels

        # Create a text area widget for input
        self.text_area = Text(self.root, bg="black", fg="white", insertbackground="white") # insert bg white inv cursor
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Create a menu bar
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        # Create a "File" dropdown menu inside menu bar
        file_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file_event)
        file_menu.add_command(label="Save", command=self.save_file_event)
        file_menu.add_separator()  # Separates options in the drop-down with a line
        file_menu.add_command(label="Compile / Run", command=self.run_file_event)

        # Create an "Edit" dropdown menu inside menu bar
        edit_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Text Area", command=self.clear_text_area)

        # Create an "Edit" dropdown menu inside menu bar
        tools_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Sensor Readings", command=self.open_sensor_readings_window)
        tools_menu.add_command(label="Command-Driven Terminal", command=self.open_command_driven_terminal)

        # Create a frame for the terminal output
        terminal_frame = tk.Frame(self.root)
        terminal_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Create a text widget for terminal output
        self.terminal = Text(terminal_frame, bg="black", fg="white", height=5)
        self.terminal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Set the terminal reference to the global variable
        set_terminal_reference(self.terminal)

        # Create a scrollbar for the terminal
        scrollbar = Scrollbar(terminal_frame, orient=tk.VERTICAL, command=self.terminal.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.terminal.config(yscrollcommand=scrollbar.set)

    # Function to open a new window called "Sensor Readings"
    def open_sensor_readings_window(self):
        sensor_window = tk.Toplevel(self.root)
        sensor_window.title("Sensor Readings")
        # Add contents to the window

    def open_command_driven_terminal(self):
        command_window = tk.Toplevel(self.root)
        command_window.title("Command-Driven Terminal")
        command_window.geometry("400x100")

        # Create a frame for the command entry
        command_frame = tk.Frame(command_window, padx=10, pady=10)
        command_frame.pack(fill=tk.BOTH, expand=True)

        # Add a label to the command-driven terminal
        label = tk.Label(command_frame, text="Enter commands:")
        label.pack(side=tk.TOP, pady=5)

        # Create a text entry widget for entering the command
        command_entry = tk.Entry(command_frame, bg="white", fg="black")
        command_entry.pack(fill=tk.BOTH, expand=True)

        def send_command_event():
            command = command_entry.get()
            parsed_command = parser.run_parser(command)
            if parsed_command:
                self.terminal_print(f"Command to be sent: {command}")
                bluetooth.send(parsed_command)
            # Clear the text entry
            command_entry.delete(0, tk.END)

        # Create a button to send the command
        send_button = tk.Button(command_frame, text="Send Command", command=send_command_event)
        send_button.pack(side=tk.BOTTOM, pady=5)

        # Bind the Enter key to send the command
        command_entry.bind("<Return>", lambda event: send_command_event())

    # Handles all GUI events for opening a file
    def open_file_event(self):
        # Open file and display result in terminal
        file = open_file()  # Call function to open file...
        # ...function returns data and a message communicating success or error
        if file:
            self.set_text_area(file)

    # Handles events for saving a file
    def save_file_event(self):
        # Save file and display result in terminal
        save_file(self.get_text_area())  # Call function to save file and pass text...

    def run_file_event(self):
        data = self.get_text_area()
        parsed_data = parser.run_parser(data)  # Syntax check and tokenize, return terminal message
        if parsed_data:
            bluetooth.send(parsed_data)

    def check_serial_event(self):
        bluetooth.check_for_serial_data()
        self.root.after(100, self.check_serial_event)

    # Clears text area
    def clear_text_area(self):
        # Clear text area
        self.text_area.delete("1.0", "end")

    def get_text_area(self):
        return self.text_area.get("1.0", "end-1c")

    def set_text_area(self, data):
        self.clear_text_area()
        self.text_area.insert("1.0", data)  # Insert file contents in text area

    def terminal_print(self, terminal_message):
        self.terminal.insert(tk.END, f"{terminal_message}\n")  # Display message in terminal
        # Auto-scroll the terminal to the bottom to display the latest message
        self.terminal.see(tk.END)

    # Runs GUI event listener
    def run(self):
        # Run the main GUI loop
        self.check_serial_event()
        self.root.mainloop()


if __name__ == "__main__":
    # Create GUI instance and run it
    gui = GUI()
    gui.run()

