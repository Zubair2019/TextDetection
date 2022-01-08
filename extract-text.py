import os
import pytesseract
from pytesseract import Output
import cv2
import json
import glob
import tqdm
from tqdm import tqdm



def extract_text(input_path, config):
    # print("Input path:", input_path)
    output_path = input_path.replace('images','annotated')
    img = cv2.imread(input_path)
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

        # filter out weak confidence text localizations
        if conf > 20:
            # display the confidence and text to our terminal
            # print("Confidence: {}".format(conf))
            # print("Text: {}".format(text))
            '''strip out non-ASCII text so we can draw the text on the image
            using OpenCV, then draw a bounding box around the text along
            with the text itself'''
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 0, 0), 3)
            cv2.imwrite(output_path, img)
    # cv2.imshow("Image", img)
    # cv2.waitKey(0)


def make_json(input_path, output_path, results):
    dictionary = {}
    text, left, top, height, width = [],[],[],[],[]
    output_path = str(output_path).split(".")[0]+'.json'
    for i in range(0, len(results["text"])):

        conf = int(results["conf"][i])
        if conf>40:
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


def compare():
    print("Hello")

if __name__ == '__main__':
    mypath = os.path.realpath(__file__)
    mypath = mypath.replace('extract-text.py','images/')
    lst = glob.glob(mypath+"*.jpg")
    for item,z in zip(lst,tqdm(range(len(lst)), desc="Writing text to json file...")):
        extract_text(item, config = ('-l eng --oem 1 --psm 3'))
   
