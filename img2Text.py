from PIL import Image
import pytesseract
import datetime

img = Image.open('W22207.jpg')
starttime = datetime.datetime.now()
text = pytesseract.image_to_string(img, lang='eng')

endtime = datetime.datetime.now()
print(text)
print((endtime - starttime).seconds)