import os
import glob
import etree.ElementTree as ET
import xmltodict
import json
import cv2
import pytesseract
from pytesseract import Output
from tqdm import tqdm
import datetime
import time


def parseXML(path):
    final_dict = {}
    with open(path) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()
    object_length = len(data_dict["annotation"]["object"])
    # print(object_length)
    del data_dict["annotation"]["folder"]
    del data_dict["annotation"]["filename"]
    del data_dict["annotation"]["source"]
    del data_dict["annotation"]["size"]
    del data_dict["annotation"]["segmented"]
    try:
        temp_path = str(path).replace('images','temp').split('.')[0]
        os.mkdir(temp_path)
    except OSError as error:
        print(error)
    for j in range(object_length):
        # del data_dict["annotation"]["object"][j]["name"]
        del data_dict["annotation"]["object"][j]["pose"]
        del data_dict["annotation"]["object"][j]["truncated"]
        del data_dict["annotation"]["object"][j]["difficult"]
        
        xmin, ymin, xmax, ymax = int(data_dict["annotation"]["object"][j]["bndbox"]["xmin"]),\
            int(data_dict["annotation"]["object"][j]["bndbox"]["ymin"]),\
                int(data_dict["annotation"]["object"][j]["bndbox"]["xmax"]),\
                    int(data_dict["annotation"]["object"][j]["bndbox"]["ymax"]),
        data_dict["annotation"]["object"][j]["name"] = cropping(data_dict["annotation"]["path"],xmin,ymin,xmax-xmin,ymax-ymin,j)


    json_data = json.dumps(data_dict)
     
    # Write the json data to output
    # json file
    mypath = os.path.realpath(__file__)
    mypath = mypath.replace('to-json.py','output/')
    # print(mypath)
    mypath = mypath+str(path).split('.')[0].split('/')[-1]+'.json'
    # print(mypath)
    with open(mypath, "w") as json_file:
        json_file.write(json_data)
        json_file.close()

def cropping(FILE, x,y,width,height,j): #Funtion to crop image and return multiple cropped images
    # print(FILE)
    img = cv2.imread(FILE)
    crop_img = img[y:y + height, x:x + width]
    config = ('-l eng --oem 1 --psm 8')
    results = pytesseract.image_to_data(crop_img, config=config, output_type=Output.DICT)
    # print(results)

    for i in range(0, len(results["text"])):
        string = results["text"][i]
        conf = int(results["conf"][i])
        # if conf > 30:
        #     print("Confidence: {}".format(conf))
        #     print("Text: {}".format(string))
        temp_path1 = str(FILE).replace('images','temp').split('.')[0]
    cv2.imwrite(temp_path1+'/'+string+".jpg", crop_img)

    return string

# Driver Code
if __name__ == "__main__":
    mypath = os.path.realpath(__file__)
    mypath = mypath.replace('to-json.py','images/')
    # print(mypath)
    lst = glob.glob(mypath+"*.xml")
    # print(lst)
    cur_time = time.time()
    # print("Start time: ",cur_time)
    for item,z in zip(lst,tqdm(range(len(lst)), desc="Extracting Text...")):
        parseXML(item)
    end_time = time.time()
    # print("End Time: ",end_time)
    print("Done!!!   Time Taken: ", end_time-cur_time)