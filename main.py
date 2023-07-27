import os
import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from tkinter import messagebox

def get_new_filename(foldername, filename, file_counter, number_pattern):
    
    parent_folder_name = os.path.basename(foldername)

    name, ext = os.path.splitext(filename)

    if number_pattern:
        new_filename = f"{parent_folder_name} {number_pattern}{file_counter}{ext}"
    else:
        new_filename = f"{parent_folder_name} {file_counter}{ext}"
    return new_filename

def rename_files_in_folders(root_dir, number_pattern, log_text, status_var):
    total_files = 0
    renamed_files = 0

    for foldername, subfolders, filenames in os.walk(root_dir):
        file_counter = {}
        for filename in filenames:
            
            if filename.endswith(".py"):
                continue

            total_files += 1

            file_path = os.path.join(foldername, filename)
            new_filename = get_new_filename(foldername, filename, file_counter.get(filename, 1), number_pattern)
            new_file_path = os.path.join(foldername, new_filename)

            if os.path.exists(new_file_path):
                while os.path.exists(new_file_path):
                    file_counter[filename] = file_counter.get(filename, 1) + 1
                    new_filename = get_new_filename(foldername, filename, file_counter[filename], number_pattern)
                    new_file_path = os.path.join(foldername, new_filename)

                file_counter[filename] += 1

            try:
                os.rename(file_path, new_file_path)
                renamed_files += 1
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_text.insert(tk.END, f"{timestamp} - ", "timestamp")
                log_text.insert(tk.END, f"Renamed: {filename} to ", "original_name")
                log_text.insert(tk.END, f"{new_filename}\n", "new_name")
                print(f"{timestamp} - Renamed: {filename} to {new_filename}")
            except Exception as e:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_text.insert(tk.END, f"{timestamp} - ", "timestamp")
                log_text.insert(tk.END, f"Error renaming {filename}: {e}\n", "error")
                print(f"{timestamp} - Error renaming {filename}: {e}")
            log_text.update_idletasks()

    status_text = f"Total Files: {total_files} | Renamed Files: {renamed_files}"
    status_var.set(status_text)

    messagebox.showinfo("Processing Complete", f"File renaming process completed!\nTotal Files: {total_files} | Renamed Files: {renamed_files}")

def toggle_pattern_entry():
    pattern_entry.config(state=tk.NORMAL if not empty_checkbox_var.get() else tk.DISABLED)
    browse_button.config(state=tk.NORMAL if (pattern_entry.get() or empty_checkbox_var.get()) else tk.DISABLED)

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        number_pattern = pattern_entry.get()
        if empty_checkbox_var.get():
            number_pattern = ""
        log_text.delete(1.0, tk.END)
        status_var.set("Processing...")
        rename_files_in_folders(folder_path, number_pattern, log_text, status_var)
        status_var.set("Ready")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Renaming Tool")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')

    label = tk.Label(root, text="Select a folder to start renaming files:")
    label.pack(pady=10)

    browse_button = tk.Button(root, text="Browse", command=browse_folder, state=tk.DISABLED)
    browse_button.pack(pady=5)

    pattern_label = tk.Label(root, text="Number Pattern:")
    pattern_label.pack(pady=5)

    empty_checkbox_var = tk.BooleanVar()
    empty_checkbox = tk.Checkbutton(root, text="Empty", variable=empty_checkbox_var, command=toggle_pattern_entry)
    empty_checkbox.pack(pady=5)

    pattern_entry = tk.Entry(root, state=tk.NORMAL)
    pattern_entry.pack(pady=5)

    log_text = ScrolledText(root, height=20, width=100)
    log_text.pack(pady=10)

    pattern_entry.bind("<KeyRelease>", lambda event: browse_button.config(state=tk.NORMAL if (pattern_entry.get() or empty_checkbox_var.get()) else tk.DISABLED))

    log_text.tag_configure("error", foreground="red")
    log_text.tag_configure("original_name", foreground="red")
    log_text.tag_configure("new_name", foreground="green")
    log_text.tag_configure("timestamp", foreground="black")

    status_var = tk.StringVar()
    status_var.set("Ready")
    status_label = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_label.pack(side=tk.BOTTOM, fill=tk.X)

    root.mainloop()