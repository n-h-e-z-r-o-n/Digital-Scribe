import tkinter as tk
from tkinter import scrolledtext

class TextEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Text Editor with Undo/Redo")
        self.geometry("600x400")

        self.text_widget = scrolledtext.ScrolledText(self, undo=True, wrap=tk.WORD)
        self.text_widget.pack(expand=True, fill=tk.BOTH)

        # Bind the keyboard shortcuts for undo and redo
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)

    def undo(self, event=None):
        try:
            self.text_widget.edit_undo()
        except tk.TclError:
            pass

    def redo(self, event=None):
        try:
            self.text_widget.edit_redo()
        except tk.TclError:
            pass

if __name__ == "__main__":
    editor = TextEditor()
    editor.mainloop()
