import os
import glob
from tqdm import tqdm
import json
from colors import *
import numpy as np

# Function reads the json files from output and annotated folder for comparison
def read_json():
	tot_gt_zones1=0 
	tot_det_zones1=0 
	misses1=0 
	false_alarm1=0
	matches1 = 0
	Match = 0
	FalseDet = 0
	Missed = 0
	metric = []
	mypath = os.path.realpath(__file__)
	gtpath = mypath.replace('compare.py','inputjson/') #Ground truth files are in output folder 
	genpath = mypath.replace('compare.py','annotated/') # Generated files are in annotted folder
	lst1 = glob.glob(gtpath+"*.json")
	lst2 = glob.glob(genpath+"*.json")
	# lst1 = ['/Users/mac/GitHub/TextDetection/inputjson/84.json']
	# lst2 = ['/Users/mac/GitHub/TextDetection/annotated/84.json']
	lst1.sort()
	lst2.sort()
	for item1,item2 in zip(lst1,lst2):
		if str(item1).split('.')[0].split('/')[-1] == str(item2).split('.')[0].split('/')[-1]:
			# print("File name:",item1)
			with open(item1, "r") as json_file:
				dict1 = json.load(json_file)
			with open(item2, "r") as json_file:
				dict2 = json.load(json_file)
			tot_gt_zones, tot_det_zones,matches, misses, false_alarm = compare_text1(dict1,dict2)
			tot_gt_zones1+=tot_gt_zones
			tot_det_zones1+= tot_det_zones
			misses1+=misses
			false_alarm1+=false_alarm
			matches1 += matches
			'''print(bcolors.OKCYAN+bcolors.BOLD+'GT Detections:--'+ str(tot_gt_zones)+'   Detections by OCR:--'+\
				str(tot_det_zones)+'  Matches:--'+str(matches)+'  Misses:--'+str(misses)+\
					'  False Detections:--'+str(false_alarm)+bcolors.ENDC)'''
			correct, falsedet, missed = compare_text(dict1,dict2)
			Match += correct
			FalseDet += falsedet
			Missed += missed
			'''print(bcolors.OKCYAN+'File:'+ str(item2)+bcolors.ENDC,bcolors.OKGREEN+'Correct:--'+\
				str(correct),bcolors.FAIL+bcolors.BOLD+'False Detecions:--'+str(falsedet)+'  Missed:--'+str(missed)+\
					' Annotated:--'+str(correct+falsedet)+bcolors.ENDC)'''
		else:
			print("File name doesn't Match")
	print(bcolors.OKCYAN+bcolors.BOLD+'Total GT Detections:--'+ str(tot_gt_zones1)+'   Total Detections by OCR:--'+\
				str(tot_det_zones1)+'  Total Matches:--'+str(matches1)+'  Total Misses:--'+str(misses1)+\
					'  Total False Alarms:--'+str(false_alarm1)+'  Correct Detections:--'+str(Match)+bcolors.ENDC)
	print(bcolors.FAIL+bcolors.BOLD+
					'Total GT Detections:--'+ str(tot_gt_zones1)+\
					'  Total Detections by OCR:--'+str(tot_det_zones1)+
					'  Total HZ Matches:--'+ str(matches1)+\
					'  Total HZ Misses by OCR:--'+ str(misses1)+\
					'  Total HZ False Alarm by OCR:--'+str(false_alarm1)+\
					'  Total splits:--'+str(10)+\
					'  Total Merges:--'+str(20)+\
					'  Correct Word Detections:--'+str(Match)+\
					'  Precision:--'+str((Match)/((Match)+false_alarm1))+\
					'  Recall:--'+str((Match)/((Match)+misses1))+\
					'  Word Error Rate:--'+str(((matches1-Match)+misses1+false_alarm1)/tot_gt_zones1)+bcolors.ENDC)
	metric.append(str('P8'))
	metric.append(str(tot_gt_zones1))
	metric.append(str(tot_det_zones1))
	metric.append(str(matches1))
	metric.append(str(misses1))
	metric.append(str(false_alarm1))
	metric.append(str(10))
	metric.append(str(20))
	metric.append(str(Match))
	metric.append(str((Match)/((Match)+false_alarm1)))
	metric.append(str((Match)/((Match)+misses1)))
	metric.append(str(((matches1-Match)+misses1+false_alarm1)/tot_gt_zones1))
	print(metric)
	write_csv(metric)
	'''print(bcolors.WARNING+bcolors.BOLD+'Match:--'+str(Match)+'  FalseDet:--'\
		+str(FalseDet)+'  Missed:--'+str(Missed)+'  Total Annotated:--'+str(Match+FalseDet)+'  Percentage Correct:--'+\
			str(((Match)/(Match+FalseDet+Missed))*100)+bcolors.ENDC)'''
	return 



#Function to compare dic1 and dic2 and return the correct and incorrect instances of text
def compare_text(dic1,dic2): 
	Nid = 0
	count = 0
	missed = 0
	# print(bcolors.WARNING+bcolors.BOLD+str(len(dic1["text"]))+bcolors.ENDC)
	for k in range(2): #second iteration to look for multiple occurences of a word
		for i in range (len(dic1["text"])):
			# print("DICT---",dic1,'------',dic2)
			
			if dic1["text"][i] in dic2["text"]:
				j = list(dic2["text"]).index(dic1["text"][i])
				box_a = [dic1["left"][i],dic1["top"][i],dic1["left"][i]+dic1["width"][i],dic1["top"][i]+dic1["height"][i]]
				box_b = [dic2["left"][j],dic2["top"][j],dic2["left"][j]+dic2["width"][j],dic2["top"][j]+dic2["height"][j]]
				# print(i,j,dic1["text"][i],dic2["text"][j],box_a,box_b, bb_intersection_over_union(box_a,box_b))
				if bb_intersection_over_union(box_a,box_b) >0.20:
					del dic2["left"][j],dic2["top"][j],dic2["width"][j],dic2["height"][j],dic2["text"][j]
					# del dic1["left"][i],dic1["top"][i],dic1["width"][i],dic1["height"][i],dic1["text"][i]
					count += 1
			else:
				if k==0:
					missed += 1
	# print(count,len(dic2["text"]),len(dic1["text"])) # 'len(dic2["text"]' represents incorect detections
	return count, len(dic2["text"]),missed

def compare_text1(dic1,dic2): 
	total_gt_zones = len(dic1["text"])
	total_det_zones = len(dic2["text"])
	matches = 0
	missed = 0
	miss = []
	false_alarm = []
	for k in range(1): #second iteration to look for multiple occurences of a word
		for i in range (len(dic1["text"])):
			# print("DICT---",dic1,'------',dic2)
			# if dic1["text"][i] in dic2["text"]:
			for j in range (len(dic2["text"])):
				box_a = [dic1["left"][i],dic1["top"][i],dic1["left"][i]+dic1["width"][i],dic1["top"][i]+dic1["height"][i]]
				box_b = [dic2["left"][j],dic2["top"][j],dic2["left"][j]+dic2["width"][j],dic2["top"][j]+dic2["height"][j]]
				# print(i,j,dic1["text"][i],dic2["text"][j],box_a,box_b, bb_intersection_over_union(box_a,box_b))
				if bb_intersection_over_union(box_a,box_b) >0.20:
					# print('|',i, '-', j, '--', bb_intersection_over_union(box_a,box_b))
					# del dic2["left"][j],dic2["top"][j],dic2["width"][j],dic2["height"][j],dic2["text"][j]
					# del dic1["left"][i],dic1["top"][i],dic1["width"][i],dic1["height"][i],dic1["text"][i]
					matches += 1
					miss.append(i)
		#print('[',total_gt_zones,'||',total_det_zones,'----',matches,'----', total_gt_zones-len(miss),'----',\
		#	total_det_zones-len(miss),']')
			
	# print(count,len(dic2["text"]),len(dic1["text"])) # 'len(dic2["text"]' represents incorect detections
	return total_gt_zones, total_det_zones, matches, total_gt_zones-len(miss), total_det_zones-len(miss)


# Function to find the intersection over union of two boxes
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

def write_csv(metric):
	# Pre-requisite - Import the writer class from the csv module
	from csv import writer
	with open('/Users/mac/Documents/Metric2.csv', 'a', newline='') as f_object:  
		# Pass the CSV  file object to the writer() function
		writer_object = writer(f_object)
		writer_object.writerow(metric)  
		f_object.close()
if __name__ == '__main__':
	read_json()
	
