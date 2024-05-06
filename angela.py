import tkinter as tk

class RoundedRectangleButton(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(highlightthickness=0)
        self.rounded_rectangle = None
        self.bind("<Configure>", self._draw_rounded_rectangle)

    def _draw_rounded_rectangle(self, event=None):
        self.delete("rounded_rectangle")
        width = self.winfo_width()
        height = self.winfo_height()
        radius = min(width, height) // 5  # Adjust the radius as needed for the desired roundness
        self.rounded_rectangle = self.create_rounded_rectangle(
            0, 0, width, height, radius, fill="lightgray", outline="black", width=2, tags="rounded_rectangle"
        )

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        return self.create_polygon(
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1,
            x1 + radius, y1,
            smooth=True, **kwargs
        )

# Example usage:
root = tk.Tk()
root.geometry("200x100")
root.config(bg="blue")

button = RoundedRectangleButton(root, width=500, height=500)
button.pack(pady=20)

root.mainloop()
