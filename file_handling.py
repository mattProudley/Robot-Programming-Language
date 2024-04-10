from tkinter import filedialog, messagebox


def save_file(text_area):
    """Function to save the text from the text area to a file."""
    # Get the text from the text area
    text = text_area.get("1.0", "end-1c")
    # Prompt the user to select a file path for saving
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    # If a file path is provided by the user
    if file_path:
        # Write the text to the selected file
        with open(file_path, "w") as f:
            f.write(text)
        # Clear the text area after saving
        text_area.delete("1.0", "end")
        # Show a message box indicating successful saving
        messagebox.showinfo("Saved", "Batch File Saved")


def open_file(text_area):
    """Function to open a file and populate the text area with its contents."""
    # Prompt the user to select a file to open
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    # If a file path is provided by the user
    if file_path:
        # Open the selected file in read mode
        with open(file_path, "r") as f:
            # Clear the current contents of the text area
            text_area.delete("1.0", "end")
            # Insert the contents of the file into the text area
            text_area.insert("1.0", f.read())
