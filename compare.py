import os
import glob
from tqdm import tqdm
import json

def read_json():
	dict1 = {}
	mypath = os.path.realpath(__file__)
	gtpath = mypath.replace('compare.py','output/')
	genpath = mypath.replace('compare.py','annotated/')
	lst1 = glob.glob(gtpath+"*.json")
	lst2 = glob.glob(genpath+"*.json")
	for item1,item2 in zip(lst1,lst2):
		if str(item1).split('.')[0].split('/')[-1] == str(item2).split('.')[0].split('/')[-1]:
			print("File name Matches")
			with open(item1, "r") as json_file:
				dict1 = json.load(json_file)
			with open(item2, "r") as json_file:
				dict2 = json.load(json_file)
			compare_text(dict1,dict2)
		else:
			print("File name doesn't Match")
		
def compare_text(dic1,dic2):
	count = 0
	for k in range(2):
		for i in range (len(dic1["text"])):
			# print("DICT---",dic1,'------',dic2)
			if dic1["text"][i] in dic2["text"]:
				j = list(dic2["text"]).index(dic1["text"][i])
				box_a = [dic1["left"][i],dic1["top"][i],dic1["left"][i]+dic1["width"][i],dic1["top"][i]+dic1["height"][i]]
				box_b = [dic2["left"][j],dic2["top"][j],dic2["left"][j]+dic2["width"][j],dic2["top"][j]+dic2["height"][j]]
				print(i,j,dic1["text"][i],dic2["text"][j],box_a,box_b, bb_intersection_over_union(box_a,box_b))
				if bb_intersection_over_union(box_a,box_b) >0.30:
					# del dic1["left"][i],dic1["top"][i],dic1["width"][i],dic1["height"][i],dic1["text"][i]
					del dic2["left"][j],dic2["top"][j],dic2["width"][j],dic2["height"][j],dic2["text"][j]
				# print(i,j,dic1["text"][i],dic2["text"][j],box_a,box_b,bb_intersection_over_union(box_a,box_b))
				count += 1
	print(count,len(dic1["text"]))
def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
	return iou






if __name__ == '__main__':
	read_json()
	
