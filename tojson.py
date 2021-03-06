import os
import glob
import etree.ElementTree as ET
import xmltodict
import json
import cv2
import pytesseract
from pytesseract import Output
from tqdm import tqdm
import random
import time
import numpy as np

''' This function takes as input the path of the xml file and deletes
the unnecessary information and saves the output as a json file
'''
def parseXML(path):
    # open the xml file for reading
    dictionary = {}
    text, left, top, height, width = [],[],[],[],[]
    with open(path) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()
    object_length = len(data_dict["annotation"]["object"])

    #The following code block created a directory for each image to store individual crops
    try:
        temp_path = str(path).replace('images','temp').split('.')[0]
        os.mkdir(temp_path)
    except OSError as error:
        print(error)

    # for loop for deleting and adding info to json
    for j in range(object_length):
        xmin, ymin, xmax, ymax = int(data_dict["annotation"]["object"][j]["bndbox"]["xmin"]),\
            int(data_dict["annotation"]["object"][j]["bndbox"]["ymin"]),\
                int(data_dict["annotation"]["object"][j]["bndbox"]["xmax"]),\
                    int(data_dict["annotation"]["object"][j]["bndbox"]["ymax"]),
        text.append(cropping(data_dict["annotation"]["path"],xmin,ymin,xmax-xmin,ymax-ymin))
        left.append(xmin)
        top.append(ymin)
        width.append(xmax-xmin)
        height.append(ymax-ymin)
    dictionary.update({"left":left})
    dictionary.update({"top":top})
    dictionary.update({"height":height})
    dictionary.update({"width":width})
    dictionary.update({"text":text})
    # print(dictionary)

    json_data = json.dumps(dictionary)
    # Write the json data to output
    mypath = os.path.realpath(__file__)
    mypath = mypath.replace('tojson.py','output/')
    # print(mypath)
    mypath = mypath+str(path).split('.')[0].split('/')[-1]+'.json'
    # print(mypath)

    #Write the json file
    with open(mypath, "w") as json_file:
        json_file.write(json_data)
        json_file.close()

'''The following function takes as input.
1.  FILE: The input image path.
2.  x: The x coordinate of top left corner of the cropped box.
3.  y: The y coordinate of top left corner of the cropped box.
4.  width:  the width of the cropped box.
5.  height: the height of the cropped box.

Saves the crooped image with the name of the detected text in the temp folder.
Also returns the detected text as output.
'''

def cropping(FILE, x,y,width,height): #Funtion to crop image and return multiple cropped images
    # print(FILE)
    img = cv2.imread(FILE)
    crop_img = img[y:y + height, x:x + width]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # gray = blur(gray)
    if check_blackness(gray) == True:
        gray = cv2.adaptiveThreshold(gray,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,5)
    else:
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, -1)
    
    gray = cv2.bitwise_not(gray)
    config = ('-l eng --oem 1 --psm 8')
    results = pytesseract.image_to_data(gray, config=config, output_type=Output.DICT)
    # print(results)

    for i in range(0, len(results["text"])):
        string = results["text"][i]
        conf = int(results["conf"][i])
        # if conf > 30:
        #     print("Confidence: {}".format(conf))
        #     print("Text: {}".format(string))
        temp_path1 = str(FILE).replace('images','temp').split('.')[0]
    cv2.imwrite(temp_path1+'/'+string+'--'+ str(random.randint(0,99))+".jpg", gray)

    return string

def check_blackness(image):
    # print("Total pixels:",image.size)
    # print("White Pixels:",np.sum(image >= 125))
    # print("Black Pixels:", np.sum(image == 0))
    if np.sum(image >= 127)/image.size > 0.7:
        # print("Image is White")
        return True
    else:
        # print("Black image")
        return False

# Driver Code
if __name__ == "__main__":
    mypath = os.path.realpath(__file__)
    mypath = mypath.replace('tojson.py','images/')
    # print(mypath)
    lst = glob.glob(mypath+"*.xml")
    cur_time = time.time()
    # print("Start time: ",cur_time)
    for item,z in zip(lst,tqdm(range(len(lst)), desc="Extracting Text...")):
        parseXML(item)
    end_time = time.time()
    # print("End Time: ",end_time)
    print("Done!!!   Time Taken: ", round(end_time-cur_time), "Seconds")