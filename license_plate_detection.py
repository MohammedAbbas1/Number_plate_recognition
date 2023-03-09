# import libararies
import cv2
import imutils
import csv
from datetime import datetime
import pytesseract
import os

# The path for the Tesseract OCR executable file on a Windows system
pytesseract.pytesseract.tesseract_cmd = ("C:/Program Files/Tesseract-OCR/tesseract.exe")
# Set the path to the folder containing the images
folder_path = 'C:/Users/Desktop/Number_plate_images/'
row_number = 1

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is an image file (.jpg)
    if filename.endswith('.jpg'):
        image_path = os.path.join(folder_path, filename)
        image = cv2.imread(image_path)
        # Load the image using OpenCV
        image = cv2.imread(os.path.join(folder_path, filename))       
        # Set the size of the image(e.g. display it)
        image = imutils.resize(image, width=988)
        #This is because the edge detection algorithm used later works on grayscale images
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #function to reduce noise while keeping the edges sharp.
        gray_image = cv2.bilateralFilter(gray_image, 11, 20, 20) 
        #Is an edge detection algorithm that detects edges in the grayscale image
        edged = cv2.Canny(gray_image, 30, 200)
        cnts,_ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        image1=image.copy()
        #Draw the contours using green colour
        cv2.drawContours(image1,cnts,-1,(0,255,0),3)
        #order based on their area and keeps only the 30 largest contours
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
        #stores the license plate contour
        screenCnt = None
        image2 = image.copy()
        #draw top contours
        cv2.drawContours(image2,cnts,-1,(0,255,0),3)
        # This code will detect the Corners of the Number Plate
        i=0
        for c in cnts:
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.025* perimeter, True)
            if len(approx) == 4: 
                screenCnt = approx
                #find the cordinates of the license plate contour
                x,y,w,h = cv2.boundingRect(c) 
                new_img=image[y:y+h,x:x+w]
                #stores the new image                
                cv2.imwrite('./'+str(i)+'.png',new_img)
                i+=1
                break
        #Draw the license plate contours on the original image
        try:           
            cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
        except cv2.error as e: 
            print("Error processing {image_path}: {e}")
            with open('extracted_text.csv', mode='a', newline="") as file:    
            # Create a CSV writer object
                writer = csv.writer(file)
            # Write the error message, image path, and date/time to the CSV file on a new line
                writer.writerow(["Error processing image {row_number}", image_path, now, e])
            row_number += 1
            continue
        # Skip to next image If error comes
        # Load the cropped image containing the number plate
        image2 = cv2.imread('0.png')
        text = pytesseract.image_to_string(image2,lang='eng')
        # Create a new folder for the cropped images
        folder_name = 'cropped_images'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # Saving the image in the every loop
        filename = '{}/cropped_image_{}.png'.format(folder_name, row_number)
        cv2.imwrite(filename,image2)
        # Apply some pre-processing to the image to improve OCR accuracy
        gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        # Remove any non-alphanumeric characters from the text
        text = ''.join(e for e in text if e.isalnum())
        # Text above the number plate Superimpose the text 
        image = cv2.putText(image, text, (x-50, y-50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        #Output given by the image
        print("License Plate :", text) 
        cv2.imshow("Number Plate Detection",image)
        filename_Detected= 'number_plate_{}.jpg'.format(folder_name, row_number)
        cv2.imwrite(filename_Detected,image)
        cv2.waitKey(0)
        # Set the initial row number to 1
        # Get the current date and time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Write the Output in CSV file in the append mode
        with open('extracted_text.csv',mode='a', newline="") as file:    
            # Create a CSV writer object
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['Row Number', 'Extracted Text', 'Date/Time', 'Image Path'])
            # Write the extracted text and date/time to the CSV file on the same line
            writer.writerow([row_number ,text ,now ,image_path])
            row_number += 1
