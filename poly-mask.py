from PIL import Image, ImageDraw ,ImageFont
import os, os.path
import cv2
import numpy

in_path ="img\\input"
out_path="img\\output"
result_path="img\\result"
script_dir = os.path.dirname(__file__)

abs_in_path = os.path.join(script_dir, in_path)
abs_out_path = os.path.join(script_dir, out_path)
abs_result_path = os.path.join(script_dir, result_path)


POLYGON_MASK1 = [
    (450,0),
    (700,0),
    (700,388),
    (710,388)
]

POLYGON_MASK2 = [ 
     (0, 0),
    (0, 488),
    (40, 488),
    (220, 0)
]

imgs = []
valid_images = [".jpg",".gif",".png",".tga"]

CROP_RECT = (50, 100, 700, 900)

# Cropping the images 
def cropper(abs_in_path ,abs_out_path,img_name):
    image = Image.open(abs_in_path)
    ImageDraw.Draw(image).polygon(POLYGON_MASK1, fill=(0, 0, 0))
    ImageDraw.Draw(image).polygon(POLYGON_MASK2, fill=(0, 0, 0))
    cropped_image = image.crop(CROP_RECT)
    cropped_image.save(abs_out_path)
    rgb_to_bgr(abs_out_path,abs_in_path,img_name)

def rgb_to_bgr(file_path,parent_path,img_name):
    image = Image.open(file_path)
    unmasked_pixels = count_unmasked_pixels(image)
    opencv_image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    edged_image = cv2.Canny(opencv_image, 100, 200)
    edge_pixels =count_edge_pixels(edged_image)
    cv2.imwrite(file_path, edged_image)
    ratio=float(edge_pixels) / float(unmasked_pixels)
    writter_text(parent_path,ratio,img_name)
  

def writter_text(file_path,ratio,img_name):
    img = Image.open(file_path)
    d = ImageDraw.Draw(img)
    fonts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app\\fonts\\abel-regular.ttf')
    font = ImageFont.truetype(fonts_path, 20)
    d.text((50,50), "Ration :%s"% ratio, fill=(255, 255, 0),font=font)
    img_out_path=os.path.join(abs_result_path, img_name)
    img.save(img_out_path)

def count_unmasked_pixels(pil_image):
    pixels = pil_image.load()
    count = 0
    for x in range(0, pil_image.size[0]):
        for y in range(0, pil_image.size[1]):
            if pixels[x, y] != (0, 0, 0):
                count = count + 1
    return count

def count_edge_pixels(opencv_image):
    count = 0
    width, height = opencv_image.shape[:2]

    for x in range(0, width):
        for y in range(0, height):
            if opencv_image[x, y] ==255:
                count = count + 3
    return count

for f in os.listdir(abs_in_path): #assuming gif
    ext = os.path.splitext(f)[1]
   # if ext.lower() not in valid_images:
    #    continue
    img_path=os.path.join(abs_in_path, f)
    img_out_path=os.path.join(abs_out_path, f)
    cropper(img_path,img_out_path,f)
    #writter_text(img_path)

fonts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts')
print fonts_path
