import tkinter as tk
from tkinter import StringVar
from tkinter import ttk
import subprocess
import json
import os

def on_key_release(event):
    """Filter items based on the typed text, but exclude arrow keys."""
    # Check if the key pressed is one of the arrow keys
    if event.keysym in ['Up', 'Down', 'Left', 'Right']:
        return  # Do nothing if the key is an arrow key
    
    query = search_var.get().lower()
    filtered_items = [(key, value) for key, value in data.items() if query in key.lower()]
    update_table(filtered_items)


def update_table(items):
    """Update the treeview with the provided items and highlight the top element."""
    for row in treeview.get_children():
        treeview.delete(row)
    
    for index, (key, value) in enumerate(items):
        treeview.insert('', tk.END, values=(key, value))
    
    # Highlight the top item if the list is not empty
    if items:
        treeview.selection_set(treeview.get_children()[0])  # Select the first item


def on_enter_pressed(event):
    """Copy the value of the top item to the clipboard using pbcopy and close the program."""
    selected_item = treeview.selection()
    if selected_item:
        top_item = treeview.item(selected_item[0])['values']
        value = top_item[1]  # Get the second column (value)
        
        # Use pbcopy to copy to clipboard
        subprocess.run("pbcopy", input=str(value).encode(), check=True)
        root.destroy()


def load_data_from_json(file_path):
    """Load data from the JSON file, return an empty dict if file is missing or invalid."""
    if not os.path.exists(file_path):
        return {}  # Return an empty dictionary if the file doesn't exist

    try:
        with open(file_path, 'r') as file:
            return json.load(file)  # Attempt to load JSON data
    except (json.JSONDecodeError, IOError) as e:
        return {}  # Return an empty dict if there's an error reading or parsing the file


def move_selection(direction):
    """Move the selection in the given direction ('up' or 'down')."""
    selected_item = treeview.selection()
    if not selected_item:
        return  # No item is selected, do nothing

    # Get the list of all items
    items = treeview.get_children()

    # Find the index of the current selected item
    current_index = items.index(selected_item[0])

    # Determine the new index based on the direction
    if direction == "up" and current_index > 0:
        new_index = current_index - 1
    elif direction == "down" and current_index < len(items) - 1:
        new_index = current_index + 1
    else:
        return  # If at the top or bottom, do nothing

    # Select the new item
    treeview.selection_set(items[new_index])
    treeview.focus(items[new_index])


# Load data from 'data.json' file
data = load_data_from_json('data.json')

# Create the main window
root = tk.Tk()
root.title("Easy Copy")

# Center the window
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

# String variable for search
search_var = StringVar()

# Search box (entry)
entry = tk.Entry(root, textvariable=search_var, font=("Arial", 14))
entry.pack(pady=10, padx=10, fill=tk.X)
entry.focus_set()

# Treeview (Table-like view)
treeview = ttk.Treeview(root, columns=("Key", "Value"), show="headings", height=15)
treeview.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Define column headings
treeview.heading("Key", text="Key")
treeview.heading("Value", text="Value")

# Populate the table with all items
update_table([(key, value) for key, value in data.items()])

# Bind events
entry.bind("<KeyRelease>", on_key_release)
entry.bind("<Return>", on_enter_pressed)
root.bind("<Up>", lambda event: move_selection("up"))
root.bind("<Down>", lambda event: move_selection("down"))

# Run the application
root.mainloop()
