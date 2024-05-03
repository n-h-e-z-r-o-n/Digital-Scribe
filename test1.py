import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Border Color Example")

    # Create a frame with a border color
    frame = tk.Frame(root, width=200, height=200, highlightbackground="blue", highlightthickness=2)
    frame.pack(padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
