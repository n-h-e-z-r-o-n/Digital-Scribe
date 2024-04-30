import base64
from PIL import Image
from io import BytesIO

def convert_base64_to_image(base64_data):
    # Remove the prefix 'data:image/jpeg;base64,' from the base64 string
    base64_data = base64_data.replace('data:image/jpeg;base64,', '')

    # Decode the base64 data
    image_data = base64.b64decode(base64_data)

    # Open the image using PIL
    image = Image.open(BytesIO(image_data))

    return image

# Example usage
base64_data = """
"""
image = convert_base64_to_image(base64_data)
image.show()  # Display the image using the default image viewer