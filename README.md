# Number_plate_recognition

##### This project is aimed at detecting license plates in images using OpenCV and Pytesseract OCR. The program will loop through all files in a specified folder containing JPG images, Identify the license plates, Crop the images to isolate the license plate, Apply OCR to the cropped image to extract the text on the license plate, And display the text on the Original image.

## Dependencies This project requires the following libraries:

- OpenCV
* Imutils
+ Csv
- Datetime
* Pytesseract

## Installation To install the required libraries, run the following command:

```
pip install opencv-python
pip install imutils
pip install csv
pip install pytesseract
```

## In addition to installing the libraries, you also need to install Tesseract OCR and set the path to the Tesseract OCR executable file in the code. The path for the Tesseract OCR executable file on a Windows system is:

```
pytesseract.pytesseract.tesseract_cmd = ("C:/Program Files/Tesseract-OCR/tesseract.exe")
```

## Usage To use this program, you need to specify the path to the folder containing the images you want to process:

```
folder_path = 'C:/Users/Desktop/Number_plate_images/'
```

## Once you have specified the folder path, run the program to detect license plates in the images:

```
python license_plate_detection.py
```

## The program will process all images in the specified folder and display the text on the original image. The text on the license plates will also be saved to a CSV file named

```
"extracted_text.csv"
```
# Results
##### License Plate Detection
![number_plate_cropped_images](https://user-images.githubusercontent.com/126225087/224005084-c536f974-080a-4cdd-b3e4-fc6ed368ca8e.jpg)
##### License Plate Detection
![number_plate_cropped_images](https://user-images.githubusercontent.com/126225087/224005814-4b3454f7-56fb-4b0a-a954-e70aa552fb9f.jpg)
##### License Plate Detection
![number_plate_cropped_images](https://user-images.githubusercontent.com/126225087/224006083-db83a7e5-a623-428c-a9f6-916a8526ccb5.jpg)

