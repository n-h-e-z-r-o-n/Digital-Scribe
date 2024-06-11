import tkinter as tk
from tkinter import messagebox


def show_popup():
    # Create a new popup window
    popup = tk.Toplevel()
    popup.title("Select an Item")

    # Set the geometry for the popup window (optional)
    popup.geometry("300x200")

    # Create a listbox widget
    listbox = tk.Listbox(popup, selectmode=tk.SINGLE)
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Add items to the listbox
    items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
    for item in items:
        listbox.insert(tk.END, item)

    # Create a function to handle item selection
    def on_select(event):
        selected_index = listbox.curselection()
        if selected_index:
            selected_item = listbox.get(selected_index)
            messagebox.showinfo("Item Selected", f"You selected: {selected_item}")
            popup.destroy()

    # Bind the listbox selection event to the on_select function
    listbox.bind("<<ListboxSelect>>", on_select)

    # Create a close button to close the popup window
    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)


def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Main Window")

    # Center the main window on the screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # Create a button to show the popup list
    popup_button = tk.Button(root, text="Show Popup", command=show_popup)
    popup_button.pack(pady=20)

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
