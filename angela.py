from PIL import Image, ImageTk
import io
import base64

def imagen(image_path, screen_width, screen_height, widget): # image processing
    def load_image():
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
        print("--",photo)
        #widget.config(image=photo)
        #widget.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected

    load_image()

imagen(r"C:\Users\HEZRON WEKESA\OneDrive\Pictures\Image.jpg", 50, 50, 0)