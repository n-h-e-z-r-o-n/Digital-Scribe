from PIL import Image

import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# Simple image to string
image_path = r"C:\Users\HEZRON WEKESA\OneDrive\Pictures\AdmissionLetter.png"
print(pytesseract.image_to_string(Image.open(image_path)))

# In order to bypass the image conversions of pytesseract, just use relative or absolute image path
# NOTE: In this case you should provide tesseract supported images or tesseract will return error


# List of available languages
print("-languages ------------------------------------------------------- \n", pytesseract.get_languages(config=''))

print(" eng -------------------------------------------------------- \n", pytesseract.image_to_string(Image.open(image_path), lang='eng'))

print("script -------------------------------------------------------- \n", pytesseract.image_to_osd(Image.open(image_path)))

# Get a searchable PDF
pdf = pytesseract.image_to_pdf_or_hocr(image_path, extension='pdf')
with open('test.pdf', 'w+b') as f:
    f.write(pdf) # pdf type is bytes by default

# Get HOCR output
hocr = pytesseract.image_to_pdf_or_hocr(image_path, extension='hocr')

# Get ALTO XML output
xml = pytesseract.image_to_alto_xml(image_path)