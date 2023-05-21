import tkinter as tk
from tkinter import filedialog

from BE.scdMain import runSCD


def validate_input(text):
    # Check if the input consists only of digits
    return text.isdigit() or text == ""

def select_directory():
    directory = filedialog.askdirectory()
    mail_directory_entry.insert(0,directory)

def run_scd_algorithm():
    path=mail_directory_entry.get()
    num_of_rotations=RF_entry.get()
    implementation_param=implementation_param_entry.get()
    k_param=K_param_entry.get()
    display_options=[]
    runSCD(path, num_of_rotations, implementation_param, k_param,display_options)

# Create the main application window
window = tk.Tk()
window.geometry("500x400")
validate_cmd = window.register(validate_input)

# directory importer
mail_directory_label = tk.Label(window, text="Select Directory:", anchor="w")
mail_directory_label.grid(row=0,column=0, padx=10, pady=10)
mail_directory_entry = tk.Entry(window)
mail_directory_entry.grid(row=0,column=1)
mail_directory = tk.Button(window, text="...", command=select_directory, anchor="w")
mail_directory.grid(row=0,column=2)

# rotating forest number of rotation - make sure only numbers are accepted
RF_label = tk.Label(window, text="Insert number of rotations for RotatingForest:")
RF_label.grid(row=1,column=0, columnspan=2, padx=10, pady=10)
RF_entry = tk.Entry(window, validate="key", validatecommand=(validate_cmd, "%P"))
RF_entry.grid(row=1,column=2)

# scd consts
SCD_title = tk.Label(window, text="Insert SCD algorithm consts:")
SCD_title.grid(row=2,column=1, padx=10, pady=10)
implementation_param_label = tk.Label(window, text="α - implementation parameter: (default=10)")
implementation_param_label.grid(row=3,column=0, columnspan=2, padx=10, pady=10)
implementation_param_entry = tk.Entry(window, validate="key", validatecommand=(validate_cmd, "%P"))
implementation_param_entry.grid(row=3,column=2)
K_param_label = tk.Label(window, text="K - number of most suspicious accounts:", anchor="w")
K_param_label.grid(row=4,column=0, columnspan=2, padx=10, pady=10)
K_param_entry = tk.Entry(window, validate="key", validatecommand=(validate_cmd, "%P"))
K_param_entry.grid(row=4,column=2)

# display modes - checkboxes
display_label = tk.Label(window, text="Display options:")
display_label.grid(row=5,column=1, padx=10, pady=10)
graph_checkbox_checked = tk.IntVar()
table_checkbox_checked = tk.IntVar()

graph_checkbox = tk.Checkbutton(window, text="Graph", variable=graph_checkbox_checked)
graph_checkbox.grid(row=6,column=0, padx=10, pady=10)
table_checkbox = tk.Checkbutton(window, text="Table", variable=table_checkbox_checked)
table_checkbox.grid(row=6,column=1)


# Create a button widget
button = tk.Button(window, text="Start", command=run_scd_algorithm)
button.grid(row=7,column=0, columnspan=3, padx=10, pady=10)

# Run the main event loop
window.mainloop()
