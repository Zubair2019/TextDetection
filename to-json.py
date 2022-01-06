import os
import glob
import etree.ElementTree as ET
import xmltodict
import json

def parseXML(path):
    final_dict = {}
    with open(path) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()
     
    # generate the object using json.dumps()
    # corresponding to json data
     
    json_data = json.dumps(data_dict)
     
    # Write the json data to output
    # json file
    mypath = os.path.realpath(__file__)
    mypath = mypath.replace('to-json.py','output/')
    print(mypath)
    mypath = mypath+str(path).split('.')[0].split('/')[-1]+'.json'
    print(mypath)
    with open(mypath, "w") as json_file:
        json_file.write(json_data)
        json_file.close()

# Driver Code
if __name__ == "__main__":
    mypath = os.path.realpath(__file__)
    mypath = mypath.replace('to-json.py','input/labelled/')
    print(mypath)
    lst = glob.glob(mypath+"*.xml")
    print(lst)
    for item in lst:
        parseXML(item)