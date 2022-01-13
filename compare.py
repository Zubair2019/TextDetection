import os
import glob
from tqdm import tqdm

def read_json():
	mypath = os.path.realpath(__file__)
	gtpath = mypath.replace('compare.py','output/')
	genpath = mypath.replace('compare.py','annotated/')
	lst1 = glob.glob(gtpath+"*.json")
	lst2 = glob.glob(genpath+"*.json")
	for item1,item2 in zip(lst1,lst2):
		print(item1,item2)
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
	
