from paddleocr import PaddleOCR,draw_ocr
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory

img_path =  r"C:\Users\HEZRON WEKESA\Downloads\34.JPG"

result = ocr.ocr(img_path, cls=True)
print("======================================================= \n\n")
text = ""
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        text += line[1][0] + "\n"
print()
print("======================================================= \n\n")
boxes = [res[0] for res in result[0]] #
texts = [res[1][0] for res in result[0]]
scores = [0 for res in result[0]]

print(texts)


import cv2 #opencv
from PIL import Image
font_path = "./Assets/latin.ttf"

image = Image.open(img_path).convert('RGB')
annotated = draw_ocr(image, boxes, texts, scores, font_path=font_path)


# show the image using matplotlib

im_show = Image.fromarray(annotated)
im_show.save('result.jpg')

