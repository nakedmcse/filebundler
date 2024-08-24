import os
import tkinter as tk
import zipfile
from tkinter import filedialog, messagebox

# Globals
folder_path = ''
output_file = ''


# Actions
def choose_folder():
    global folder_path, output_file, output_text, info_label
    folder_path = filedialog.askdirectory()
    if folder_path:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if filename.endswith('.txt') or filename.endswith('.TXT'):
                with open(file_path, 'r') as file:
                    output_file += file.read()
                    output_text.config(state=tk.NORMAL)
                    output_text.insert(tk.END, f'Added contents of {filename}\n')
                    output_text.config(state=tk.DISABLED)
            elif filename.endswith('.zip') or filename.endswith('.ZIP'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    for zip_info in zip_ref.infolist():
                        if zip_info.filename.endswith('.txt'):
                            with zip_ref.open(zip_info) as file:
                                output_file += file.read().decode('utf-8')
                                output_text.config(state=tk.NORMAL)
                                output_text.insert(tk.END, f'Added contents of {filename}\n')
                                output_text.config(state=tk.DISABLED)

    info_label.config(text=f'({len(output_file.splitlines())} lines)')


def save_file():
    global output_file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(output_file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")


def clear_file():
    global output_file, output_text
    output_file = ""
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, 'Cleared output file\n')
    output_text.config(state=tk.DISABLED)
    info_label.config(text='(0 lines)')


# Render Window
root = tk.Tk()
root.title("File Bundler")
root.geometry("800x400")

# Frames
button_upper_frame = tk.Frame(root)
button_upper_frame.pack(fill=tk.X)
button_lower_frame = tk.Frame(root)
button_lower_frame.pack(fill=tk.X)
results_frame = tk.Frame(root, pady=15)
results_frame.pack(fill=tk.BOTH)

# Buttons
folder_label = tk.Label(button_upper_frame, text="Folder:")
folder_label.pack(side="left", padx=5)
folder_var = tk.Entry(button_upper_frame, width=65)
folder_var.pack(side="left", padx=5)
choose_folder_button = tk.Button(button_upper_frame, text="Add Files", command=choose_folder)
choose_folder_button.pack(side="left", padx=5)

save_button = tk.Button(button_lower_frame, text="Save Combined File", command=save_file)
save_button.pack(side="left", padx=5)
clear_button = tk.Button(button_lower_frame, text="Clear File", command=clear_file)
clear_button.pack(side="left", padx=5)
info_label = tk.Label(button_lower_frame, text="(0 lines)")
info_label.pack(side="left", padx=5)

# Results
output_text = tk.Text(results_frame, state=tk.DISABLED)
output_text.pack(side="left", fill=tk.BOTH, expand=True, padx=5)

root.mainloop()
