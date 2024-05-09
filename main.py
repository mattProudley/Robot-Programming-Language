# GUI constructor and main loop, handles events
import tkinter as tk
from tkinter import Menu, Text, Scrollbar
from file_handling import save_file, open_file
import parser
import bluetooth
from utils import set_terminal_reference, set_sensor_terminal_reference

class GUI:
    def __init__(self):
        # Initialize main Tkinter window
        self.root = tk.Tk()
        self.text_area = None  # Initialize text area as None initially
        self.terminal = None  # Initialize terminal as None initially
        self.sensor_terminal = None
        self.gui_constructor()  # Build GUI components
        self.setup_bluetooth()  # Set up Bluetooth serial port

    def setup_bluetooth(self):
        # Initialize Bluetooth serial port for communication
        bluetooth.setup_serial_port()

    def gui_constructor(self):
        # Set window title and size
        self.root.title("Robot Programmer")
        self.root.geometry("800x600")

        # Create text area for user input
        self.text_area = Text(self.root, bg="black", fg="white", insertbackground="white")
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Create menu bar and configure main window
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        # Create "File" menu with options
        file_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file_event)
        file_menu.add_command(label="Save", command=self.save_file_event)
        file_menu.add_separator()  # Separator line
        file_menu.add_command(label="Compile / Run", command=self.run_file_event)

        # Create "Edit" menu with options
        edit_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Text Area", command=self.clear_text_area)

        # Create "Tools" menu with options
        tools_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Sensor Readings", command=self.open_sensor_readings_window)
        tools_menu.add_command(label="Command-Driven Terminal", command=self.open_command_driven_terminal)

        # Create terminal frame at the bottom of the window
        terminal_frame = tk.Frame(self.root)
        terminal_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Create text widget for terminal output
        self.terminal = Text(terminal_frame, bg="black", fg="white", height=5)
        self.terminal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        set_terminal_reference(self.terminal)  # Set terminal global reference for utils print_to_terminal()

        # Create scrollbar for terminal
        scrollbar = Scrollbar(terminal_frame, orient=tk.VERTICAL, command=self.terminal.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.terminal.config(yscrollcommand=scrollbar.set)

    def open_sensor_readings_window(self):
        # Create a new window for sensor readings
        sensor_window = tk.Toplevel(self.root)
        sensor_window.title("Sensor Readings")
        sensor_window.geometry("400x300")  # Set the size of the pop-up window

        # Create a frame for sensor readings content
        sensor_frame = tk.Frame(sensor_window, padx=10, pady=10)
        sensor_frame.pack(fill=tk.BOTH, expand=True)

        # Create a text widget for displaying sensor readings (terminal-like behavior)
        self.sensor_terminal = Text(sensor_frame, bg="black", fg="white", height=5)
        self.sensor_terminal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        set_sensor_terminal_reference(self.sensor_terminal)

        # Create a scrollbar for the sensor terminal
        self.scrollbar = Scrollbar(sensor_frame, orient=tk.VERTICAL, command=self.sensor_terminal.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sensor_terminal.config(yscrollcommand=self.scrollbar.set)

        def export_sensor_readings_event():
            # Retrieve the content of the text widget
            data = self.sensor_terminal.get("1.0", tk.END)
            # Pass the data to a file handling function (save_file)
            save_file(data)

        # Create a button at the bottom of the window to export data from the terminal
        export_button = tk.Button(sensor_window, text="Export Data", command=export_sensor_readings_event)
        export_button.pack(side=tk.BOTTOM, pady=10)  #

    def open_command_driven_terminal(self):
        # Create a new window for the command-driven terminal
        command_window = tk.Toplevel(self.root)
        command_window.title("Command-Driven Terminal")
        command_window.geometry("400x100")

        # Create frame for command entry
        command_frame = tk.Frame(command_window, padx=10, pady=10)
        command_frame.pack(fill=tk.BOTH, expand=True)

        # Add label to the command-driven terminal
        label = tk.Label(command_frame, text="Enter commands:")
        label.pack(side=tk.TOP, pady=5)

        # Create text entry widget for entering commands
        command_entry = tk.Entry(command_frame, bg="white", fg="black")
        command_entry.pack(fill=tk.BOTH, expand=True)

        # Define event function to send commands
        def send_command_event():
            command = command_entry.get() # Get command/s from text box
            parsed_command = parser.run_parser(command) # Parse command, returns tokens
            if parsed_command: # If no syntax errors
                self.terminal_print(f"Command to be sent: {command}") # Print command to be sent
                bluetooth.send(parsed_command) # Send tokens via BT
            command_entry.delete(0, tk.END)  # Clear the text entry widget

        # Create button to send commands
        send_button = tk.Button(command_frame, text="Send Command", command=send_command_event)
        send_button.pack(side=tk.BOTTOM, pady=5)

        # Bind Enter key to send commands
        command_entry.bind("<Return>", lambda event: send_command_event())

    def open_file_event(self):
        # Open file and display content in the text area
        file = open_file()  # Function to open file and return data
        if file:
            self.set_text_area(file)  # Set file data in text area

    def save_file_event(self):
        # Save content of text area to a file
        save_file(self.get_text_area())  # Save text area content using utility function

    def run_file_event(self):
        data = self.get_text_area() # Get data from text area
        parsed_data = parser.run_parser(data)  # Parse text area content, returns tokens
        if parsed_data:
            bluetooth.send(parsed_data)  # Send parsed data over Bluetooth

    def check_serial_data_event(self):
        # Check for serial data, print if available, and schedule next check
        bluetooth.check_for_serial_data()
        self.root.after(100, self.check_serial_data_event)  # Schedule next check in 100ms

    def clear_text_area(self):
        # Clear the text area
        self.text_area.delete("1.0", "end")

    def get_text_area(self):
        # Get content of the text area
        return self.text_area.get("1.0", "end-1c")

    def set_text_area(self, data):
        # Set the text area content with the provided data
        self.clear_text_area()
        self.text_area.insert("1.0", data)  # Insert data in text area

    def terminal_print(self, terminal_message):
        # Print message in the terminal
        self.terminal.insert(tk.END, f"{terminal_message}\n")
        self.terminal.see(tk.END)  # Auto-scroll terminal to the latest message

    def run(self):
        # Run the main event loop of the GUI
        self.check_serial_data_event()  # Routinely check for serial data
        self.root.mainloop()  # Start the main loop


if __name__ == "__main__":
    # Create and run GUI / Main instance
    gui = GUI()
    gui.run()
