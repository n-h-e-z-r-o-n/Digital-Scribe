import pywhatkit as kit
from PIL import Image
import pytesseract

im = Image.open(r"C:\Users\HEZRON WEKESA\Downloads\after_2-2843848629.JPG")

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
text = pytesseract.image_to_string(im, lang='eng')


kit.text_to_handwriting(text, rgb=(200,80,0), save_to="./nintendoHW.jpg")