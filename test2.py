import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil

# File system path for storing documents
DOCUMENT_PATH = 'documents'

def create_document_folder():
    if not os.path.exists(DOCUMENT_PATH):
        os.makedirs(DOCUMENT_PATH)

def show_document_manager():
    document_window = tk.Toplevel(root)
    document_window.title("Document Manager")

    # Create a frame to hold the document list
    document_frame = ttk.Frame(document_window)
    document_frame.pack(pady=10)

    # Create a scrollable treeview to display the documents
    document_tree = ttk.Treeview(document_frame)
    document_tree["columns"] = ("name", "size", "date")
    document_tree.column("#0", width=200)
    document_tree.column("name", width=200, anchor="w")
    document_tree.column("size", width=100, anchor="w")
    document_tree.column("date", width=150, anchor="w")
    document_tree.heading("#0", text="Name", anchor="w")
    document_tree.heading("name", text="Name", anchor="w")
    document_tree.heading("size", text="Size", anchor="w")
    document_tree.heading("date", text="Date Modified", anchor="w")
    document_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a vertical scrollbar to the treeview
    document_scrollbar = ttk.Scrollbar(document_frame, orient=tk.VERTICAL, command=document_tree.yview)
    document_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    document_tree.configure(yscrollcommand=document_scrollbar.set)

    # Load documents from the file system
    load_documents(document_tree)

    # Create buttons for adding, deleting, and uploading documents
    button_frame = ttk.Frame(document_window)
    button_frame.pack(pady=10)

    add_button = ttk.Button(button_frame, text="Add Document", command=lambda: add_document(document_tree))
    add_button.pack(side=tk.LEFT, padx=5)

    delete_button = ttk.Button(button_frame, text="Delete Document", command=lambda: delete_document(document_tree))
    delete_button.pack(side=tk.LEFT, padx=5)

    upload_button = ttk.Button(button_frame, text="Upload Document", command=lambda: upload_document(document_tree))
    upload_button.pack(side=tk.LEFT, padx=5)

def load_documents(tree):
    for folder, _, files in os.walk(DOCUMENT_PATH):
        for file in files:
            file_path = os.path.join(folder, file)
            file_size = os.path.getsize(file_path)
            file_date = os.path.getmtime(file_path)
            tree.insert("", "end", text=file, values=(file, format_file_size(file_size), format_date(file_date)))

def format_file_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024 ** 2:
        return f"{size // 1024} KB"
    elif size < 1024 ** 3:
        return f"{size // (1024 ** 2)} MB"
    else:
        return f"{size // (1024 ** 3)} GB"

def format_date(timestamp):
    import datetime
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def add_document(tree):
    file_path = filedialog.askopenfilename(title="Select Document")
    if file_path:
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(DOCUMENT_PATH, file_name)
        shutil.copy(file_path, dest_path)
        file_size = os.path.getsize(dest_path)
        file_date = os.path.getmtime(dest_path)
        tree.insert("", "end", text=file_name, values=(file_name, format_file_size(file_size), format_date(file_date)))

def delete_document(tree):
    selected_item = tree.selection()
    if selected_item:
        file_name = tree.item(selected_item, "text")
        file_path = os.path.join(DOCUMENT_PATH, file_name)
        answer = messagebox.askyesno("Delete Document", f"Are you sure you want to delete '{file_name}'?")
        if answer:
            os.remove(file_path)
            tree.delete(selected_item)

def upload_document(tree):
    file_path = filedialog.askopenfilename(title="Select Document to Upload")
    if file_path:
        # Implement your logic to upload the document to a server or cloud storage
        pass

# Create the main window
root = tk.Tk()
root.title("Digital Scribe")

# Create the Document Management button
document_button = ttk.Button(root, text="Document Manager", command=show_document_manager)
document_button.pack(pady=10)

# Create the document folder if it doesn't exist
create_document_folder()

root.mainloop()