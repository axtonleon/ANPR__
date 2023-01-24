from django.shortcuts import render
import matplotlib.pyplot as plt
import cv2
import numpy as np
from django.core.files.base import ContentFile
import imutils
import easyocr
from PIL import Image
from .models import Posts,MyImage
import os

# Create your views here.
def index(request):
	return render(request, 'index.html')
def upload(request):
    if request.method == 'POST':
        imgs = request.FILES.get("licence_upload")
        img = _grab_image(stream=request.FILES["licence_upload"])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
        edged = cv2.Canny(bfilter, 30, 200) #Edge detection
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0,255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)
        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]
        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)
        text = result[0][-2]
        print(text)
        font = cv2.FONT_HERSHEY_SIMPLEX
        res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
        res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
        image2 =  cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        cv2.imwrite("media/licence_images/image.jpeg", image2)
        url ="media/licence_images/image.jpeg"
        create_image(url)
        new_post = Posts.objects.create(image=imgs, licence_number=text)
        new_post.save()
        posts = Posts.objects.all()
        myImage = MyImage.objects.all()
        return render(request,'index.html',{"Post": posts,"myImage": myImage })       
    else:
        return render(request,'index.html')


def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        image = cv2.imread(path)
    # otherwise, the image does not reside on disk
    else:   
        # if the URL is not None, then download the image
        if url is not None:
            resp = urllib.request.urlopen(url)
            data = resp.read()
        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            data = stream.read()
        # convert the image to a NumPy array and then read it into
        # OpenCV format
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
    # return the image
    return image


def create_image(url):
    # Read the image using cv2
    img = cv2.imread(url)
    # Encode image to png
    _, img_encoded = cv2.imencode('.png', img)
    # Create a model instance
    new_image = MyImage()
    # Set the image field to the encoded image
    new_image.image.save("img.png", ContentFile(img_encoded.tostring()), save=True)

