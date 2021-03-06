import os
import pytesseract
from pytesseract import Output
import cv2
import json
import glob
import tqdm
from tqdm import tqdm
from compare import *
import numpy as np
#P1 P2 P3 P4 P5 P6 P7 P8 P9 P10 P11 P12 P13 P14 P15 P16 P17 P18

def extract_text(input_path, config):
    # print("Input path:", input_path)
    output_path = input_path.replace('inputimages','annotated')
    img = cv2.imread(input_path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    '''------Blurring Operations-------'''
    # img = cv2.blur(img,(5,5))
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.medianBlur(img, 3)
    # img = cv2.bilateralFilter(img,9,75,75)
    
    # _, img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    # _, img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    # _, img = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
    # _, img = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
    # _, img = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)

    # _,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    # img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    # img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

    # _,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # gray = blur(gray)
    if check_blackness(img) == True:
        img = cv2.adaptiveThreshold(img,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    else:
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)

    '''if check_blackness(img) == True:
        _,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    else:
        _,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)'''
    
    img = cv2.bitwise_not(img)





    results = pytesseract.image_to_data(img, config=config, output_type=Output.DICT)
    # print(results)
    make_json(input_path, output_path, results)
    for i in range(0, len(results["text"])):
        # extract the bounding box coordinates of the text region from the current result
        x = results["left"][i]
        y = results["top"][i]
        w = results["width"][i]
        h = results["height"][i]

        # extract the OCR text itself along with the confidence of the text localization
        text = results["text"][i]
        conf = int(results["conf"][i])
        # print(text,conf)
        # filter out weak confidence text localizations
        if conf > 70:
            # display the confidence and text to our terminal
            # print("Confidence: {}".format(conf))
            # print("Text: {}".format(text))
            '''strip out non-ASCII text so we can draw the text on the image
            using OpenCV, then draw a bounding box around the text along
            with the text itself'''
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.6, (128, 128, 0), 3)
        # cv2.imwrite(output_path, img)
    # cv2.imshow("Image", img)
    # cv2.waitKey(0)


def make_json(input_path, output_path, results):
    dictionary = {}
    text, left, top, height, width = [],[],[],[],[]
    output_path = str(output_path).split(".")[0]+'.json'
    for i in range(0, len(results["text"])):

        conf = int(results["conf"][i])
        if conf>80:
            text.append(results["text"][i])
            left.append(results["left"][i])
            top.append(results["top"][i])
            width.append(results["width"][i])
            height.append(results["height"][i])
    dictionary.update({"left":left})
    dictionary.update({"top":top})
    dictionary.update({"height":height})
    dictionary.update({"width":width})
    dictionary.update({"text":text})
    json_data = json.dumps(dictionary)
    with open(output_path, "w") as json_file:
        json_file.write(json_data)
        json_file.close()


def check_blackness(image):
    # print("Total pixels:",image.size)
    # print("White Pixels:",np.sum(image >= 125))
    # print("Black Pixels:", np.sum(image == 0))
    if np.sum(image >= 127)/image.size > 0.70:
        print("Image is White")
        return True
    else:
        print("Black image")
        return False

if __name__ == '__main__':
    mypath = os.path.realpath(__file__)
    mypath = mypath.replace('extracttext.py','inputimages/')
    lst = glob.glob(mypath+"*.jpg")
    for item,z in zip(lst,tqdm(range(len(lst)), desc="Writing text to json file...")):
        extract_text(item, config = ('-l eng --oem 1 --psm 12'))
    # exec('python compare.py')
   
