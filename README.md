# Monitoring Road Traffic with Python

Last page update: **17/04/2018**

Last version: **1.0.0** 

Hello everyone,
We want to monitor traffic with python. For this, we will take images as input.
There is a lot of content in this image that is not relevant to the amount of 
traffic in it so we want to mask and cropping the images.  


Installation pre-requisites & running 
----------------------------------------
For running this project we need and python 2.7.14 installed on our machine. 
Its important to install 
	Install python 2.7.14  on Windows
	Install OpenCV-Python in Windows 
	( http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html)
	Installing PIL 
	
	#No need to specify any directory  for this project .

	
Project Structure 
-------------------
	 Project/
	|	
	|-- app/
	|   |-- img/
	|   |   |--input
	|   |   |--output_mask
	|   |   |-- result 
	|   |-- fonts
	|   |---test
	|	| 	|--poly-mask 
	|   |-- vehicle-ratio.py
	|
	|-- setup.py
	|-- README

Image Segmentation
-----------------

	Use PIL.ImageDraw to fill in a black polygon and crop the images. 
	Use numpy to convert the image from PIL format to OpenCV. Apply the Canny edge detection algorithm.

	def cropper(abs_in_path ,abs_out_path,img_name):
    image = Image.open(abs_in_path)
    ImageDraw.Draw(image).polygon(POLYGON_MASK1, fill=(0, 0, 0))
    ImageDraw.Draw(image).polygon(POLYGON_MASK2, fill=(0, 0, 0))
    cropped_image = image.crop(CROP_RECT)
    cropped_image.save(abs_out_path)

<p align="center">
  <img src="https://github.com/mostafiz57/vehicle-ratio/blob/master/img/input/Bannani-1.5-2%20-1-mon.jpg" border="0" />
</p>

	Convert the image RGB to BGR, using the code 
	
	def rgb_to_bgr(file_path,parent_path,img_name):
    image = Image.open(file_path)
    unmasked_pixels = count_unmasked_pixels(image)
    opencv_image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    edged_image = cv2.Canny(opencv_image, 100, 200)
    edge_pixels =count_edge_pixels(edged_image)
    cv2.imwrite(file_path, edged_image)

	After extraction of frames, the image was converted into gray scale so that the processing of the image becomes simpler. 
	Each color pixel of image is described by three intensities of red (R), blue (B) and green (G).The ratio of ratio of white 
	pixels to black pixels,remember that some of the pixels from the image were black already from the polygon mask.
	
<p align="center">
  <img src="https://github.com/mostafiz57/vehicle-ratio/blob/master/img/output_mask/Bannani-1.5-2%20-1-mon.jpg" border="0" />
</p>
	
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
	
<p align="center">
  <img src="https://github.com/mostafiz57/vehicle-ratio/blob/master/img/result/Bannani-8-9%20-1-sun.jpg" border="0" />
</p>


