import tkinter as tk
from tkinter import Menu
from file_handling import save_file, open_file

# Create the main window
root = tk.Tk()
root.title("Robot Programmer")  # Set the title of the window

# Create a text area for input
text_area = tk.Text(root, bg="black", fg="white")  # Black text area with white text
text_area.pack(fill=tk.BOTH, expand=True)  # Expand the text area to fill the window

# Create a menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Create a "File" dropdown menu
file_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save", command=save_file(text_area))
file_menu.add_command(label="Open", command=open_file(text_area))

# Run the application
root.mainloop()
