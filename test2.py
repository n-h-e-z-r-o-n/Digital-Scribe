import tkinter as tk
from tkinter import messagebox
import requests
from tkinter import filedialog

def download_file(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Prompt user to select a location to save the file
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                messagebox.showinfo("Success", "File downloaded successfully!")
            else:
                messagebox.showwarning("Warning", "No file selected!")
        else:
            messagebox.showerror("Error", "Failed to download file. URL may be invalid or inaccessible.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def download():
    url = entry_url.get()
    if url:
        download_file(url)
    else:
        messagebox.showwarning("Warning", "Please enter a valid URL.")

# Create Tkinter window
window = tk.Tk()
window.title("File Downloader")

# Create URL entry field
entry_url = tk.Entry(window, width=50)
entry_url.grid(row=0, column=0, padx=10, pady=10)

# Create download button
btn_download = tk.Button(window, text="Download", command=download)
btn_download.grid(row=0, column=1, padx=10, pady=10)

# Run the Tkinter event loop
window.mainloop()
