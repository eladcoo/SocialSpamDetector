import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
from BE.scdMain import run_algorithm
from UI.tableDisplay import display_as_table
from tkinter import messagebox

def validate_input(text):
    # Check if the input consists only of digits
    return text.isdigit() or text == ""


def validate_implementation_param(text):
    if text:
        return text.isdigit()
    return True

def validate_all_inputs():
    path = mail_directory_entry.get()
    if not path:
        messagebox.showerror("Error", "Please choose a directory")
        return False
    num_of_rotations_value = RF_entry.get()
    if not num_of_rotations_value:
        messagebox.showerror("Error", "Please choose a number of rotations")
        return False
    k_param_value = K_param_entry.get()
    if not k_param_value:
        messagebox.showerror("Error", "Please choose how many suspected accounts to return")
        return False
    if not table_checkbox_checked.get() and not graph_checkbox_checked.get():
        messagebox.showerror("Error", "Please choose a display option")
        return False
    return True

def select_directory():
    directory = filedialog.askdirectory()
    mail_directory_entry.insert(0, directory)

def initiate_loading():
    # Create a label for the loading wheel
    loading_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
    loading_wheel.grid(row=8, column=2, padx=10, pady=10)
    loading_wheel.start()
    start_button['state'] = tk.DISABLED
def execute_backend():
    if validate_all_inputs():
        path = mail_directory_entry.get()
        num_of_rotations = int(RF_entry.get())
        implementation_param_value = implementation_param_entry.get()
        if implementation_param_value:
            implementation_param = int(implementation_param_value)
        else:
            implementation_param = 10
        k_param = int(K_param_entry.get())
        should_export_graph = True if graph_checkbox_checked.get() else False
        initiate_loading()
        print("values for algorithm:", path, num_of_rotations, implementation_param, k_param, should_export_graph)
        backend_thread = threading.Thread(target=run_scd_algorithm, args=(path, num_of_rotations, implementation_param, k_param, should_export_graph))
        backend_thread.start()
def run_scd_algorithm(path, num_of_rotations, implementation_param, k_param, should_export_graph):
    suspect_list = run_algorithm(path, num_of_rotations, implementation_param, k_param, should_export_graph)
    loading_label.grid_remove()
    loading_wheel.stop()
    loading_wheel.grid_remove()
    start_button['state'] = tk.NORMAL
    if table_checkbox_checked.get():
        display_as_table(suspect_list)

# Create the main application window
window = tk.Tk()
window.geometry("500x400")
validate_cmd = window.register(validate_input)

# directory importer
mail_directory_label = tk.Label(window, text="Select Directory:", anchor="w")
mail_directory_label.grid(row=0, column=0, padx=10, pady=10)
mail_directory_entry = tk.Entry(window)
mail_directory_entry.grid(row=0, column=1)
mail_directory = tk.Button(window, text="...", command=select_directory, anchor="w")
mail_directory.grid(row=0, column=2)

# rotating forest number of rotation - make sure only numbers are accepted
RF_label = tk.Label(window, text="Insert number of rotations for RotatingForest:")
RF_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
RF_entry = tk.Entry(window, validate="key", validatecommand=(validate_cmd, "%P"))
RF_entry.grid(row=1, column=2)

# scd consts
SCD_title = tk.Label(window, text="Insert SCD algorithm consts:")
SCD_title.grid(row=2, column=1, padx=10, pady=10)
implementation_param_label = tk.Label(window, text="α - implementation parameter: (default=10)")
implementation_param_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
implementation_param_entry = tk.Entry(window, validate="key", validatecommand=(validate_implementation_param, "%P"))
implementation_param_entry.grid(row=3, column=2)
K_param_label = tk.Label(window, text="K - number of most suspicious accounts:", anchor="w")
K_param_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
K_param_entry = tk.Entry(window, validate="key", validatecommand=(validate_cmd, "%P"))
K_param_entry.grid(row=4, column=2)

# display modes - checkboxes
display_label = tk.Label(window, text="Display options:")
display_label.grid(row=5, column=1, padx=10, pady=10)
graph_checkbox_checked = tk.BooleanVar()
table_checkbox_checked = tk.BooleanVar()

graph_checkbox = tk.Checkbutton(window, text="Graph", variable=graph_checkbox_checked)
graph_checkbox.grid(row=6, column=0, padx=10, pady=10)
table_checkbox = tk.Checkbutton(window, text="Table", variable=table_checkbox_checked)
table_checkbox.grid(row=6, column=1)

# Create a button widget
start_button = tk.Button(window, text="Start", command=execute_backend)
start_button.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

# Create loading
loading_label = ttk.Label(window, text="Loading...")
loading_wheel = ttk.Progressbar(window, mode="indeterminate")

# Run the main event loop
window.mainloop()
