import tkinter as tk

class PopupList(tk.Toplevel):
    def __init__(self, parent, items):
        super().__init__(parent)
        self.title("Popup List")
        self.geometry("200x200")
        self.withdraw()  # Hide the popup initially

        # Remove title bar
        self.overrideredirect(True)

        # Create a listbox
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Populate the listbox with items
        for item in items:
            self.listbox.insert(tk.END, item)

        # Bind selection event
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

    def show(self, x, y):
        self.geometry(f"+{x}+{y}")
        self.deiconify()

    def hide(self):
        self.withdraw()

    def on_select(self, event):
        selected_indices = self.listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_item = self.listbox.get(selected_index)
            print(f"Selected: {selected_item}")
            self.hide()

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Application")
        self.geometry("300x200")

        self.popup = PopupList(self, ["Option 1", "Option 2", "Option 3"])

        # Button to show the popup list
        self.button = tk.Button(self, text="Show Popup", command=self.show_popup)
        self.button.pack(pady=20)

    def show_popup(self):
        x = self.winfo_x() + self.button.winfo_x() + self.button.winfo_width()
        y = self.winfo_y() + self.button.winfo_y()
        self.popup.show(x, y)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
