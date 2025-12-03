from PIL import Image
import os

files = ["C:/Users/Nicola/Downloads/bird1.png", "C:/Users/Nicola/Downloads/bird2.png", "C:/Users/Nicola/Downloads/bird3.png"]


for f in files:
    img = Image.open(f)
    img_cropped = img.crop(img.getbbox())

    filename = os.path.basename(f)
    outname = "cropped_" + filename

    img_cropped.save(outname)
    print("Saved:", outname)
