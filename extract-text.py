import os
import pytesseract
from pytesseract import Output
import cv2



def extract_text(input_path, config):
    print(input_path)
    mypath = input_path.replace('images','annotated')
    img1 = cv2.imread(input_path)
    img = img1.copy()
    cv2.imwrite(mypath, img)

    '''
    results = pytesseract.image_to_data(img, config=config, output_type=Output.DICT)
    # print(results)

    for i in range(0, len(results["text"])):
        # extract the bounding box coordinates of the text region from the current result
        x = results["left"][i]
        y = results["top"][i]
        w = results["width"][i]
        h = results["height"][i]

        # extract the OCR text itself along with the confidence of the text localization
        text = results["text"][i]
        conf = int(results["conf"][i])
        # print(results)
        # print("Confidence: {}".format(conf))
        # print("Text: {}".format(text))

        # filter out weak confidence text localizations
        if conf > 10:
            # cv2.imwrite("/Users/mac/Data/TMP2/" + str(b) + '-' + str(j) + ".jpg", cropped)
            # text = text + ' '
            # display the confidence and text to our terminal
            print("Confidence: {}".format(conf))
            print("Text: {}".format(text))
        

            strip out non-ASCII text so we can draw the text on the image
            using OpenCV, then draw a bounding box around the text along
            with the text itself
            string = "".join([c if ord(c) < 128 else "" for c in string]).strip()
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 0, 0), 3) '''
        















if __name__ == '__main__':
    mypath = os.path.realpath(__file__)
    print(mypath)
    mypath = mypath.replace('extract-text.py','images/')
    print(mypath)
    extract_text(mypath+'1.jpg', config = ('-l eng --oem 1 --psm 8'))