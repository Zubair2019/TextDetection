from asyncio.format_helpers import extract_stack
import cv2
import os
import glob
from tqdm import tqdm


def crop_text(path):
    out_pth = '/Users/mac/GitHub/TextDetection/images/'
    filename = str(path).split('/')[-1]
    img = cv2.imread(path)
    crop_img = img[100:100 + 2300, 0:0 + 1080]
    cv2.imwrite(out_pth+filename, crop_img)







if __name__ == '__main__':
    lst = glob.glob('/Users/mac/Documents/input/'+"*.jpg")
    for item,z in zip(lst,tqdm(range(len(lst)), desc="Writing text to json file...")):
        crop_text(item)