from PIL import Image, ImageTk
import io
import base64
import tkinter as tk

def image_to_byte_string(image_path):
    with open(image_path, "rb") as image_file:
        byte_string = base64.b64encode(image_file.read()).decode('utf-8')
    return byte_string


def imagen(image_path, screen_width, screen_height, widget): # image processing
    def load_image():
        global User_Image
        try:
            image = Image.open(image_path)
        except Exception as e:
            try:
                image = Image.open(io.BytesIO(image_path))
            except Exception as e:
                print(e)
                binary_data = base64.b64decode(image_path)  # Decode the string
                image = Image.open(io.BytesIO(binary_data))

        image = image.resize((screen_width, screen_height), Image.LANCZOS)

        photo = ImageTk.PhotoImage(image)

        widget.config(image=photo)
        widget.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected

    load_image()



root = tk.Tk()

lanb = tk.Label(root, text="👤", font=("Forte", 100))
lanb.place(relwidth=1,relheight=1)

User_Image = image_to_byte_string(r"C:\Users\HEZRON WEKESA\OneDrive\Pictures\Image.jpg")

#imagen(str(User_Image), 500, 500,lanb)


root.mainloop()