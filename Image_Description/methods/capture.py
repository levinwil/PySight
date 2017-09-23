import cv2
import time
import tinys3
from PIL import Image

'''takes a picture and writes it to fileName, returns fileName'''
def take_photo(fileName):
    cap = cv2.VideoCapture(0)
    for _ in range(10):
        _, img = cap.read()
    cv2.imwrite(fileName, img)
    return fileName

'''takes a photo and uploads it to s3 under a random fileName, return fileName'''
def take_photo_and_upload_img():
    conn = tinys3.Connection("AKIAIJV4A2VRU7RAALSA","/OwQ9zmhaefHmoSiqLJxwB56K4qUWIucAZxOpm5P")
    fileNameShort = str(int(time.time())) + ".jpg"
    fileName = "../Image_Description/static/uploads/" + fileNameShort
    take_photo(fileName)
    img_file = open(fileName, 'rb')
    conn.upload(fileNameShort,img_file,'pisight')
    return fileNameShort

'''takes a photo and uploads it to s3 under a given filename, returns fileName'''
def upload_img_file(fileName):
    conn = tinys3.Connection("AKIAIMOCMF27GH7SBNXQ","B4hv2jwr9jBzRN8el+2BOvFlXHHZ1N5l4q88Sgma")
    fileNameLong = "../Image_Description/static/uploads/" + fileName
    img_file = open(fileNameLong, 'rb')
    conn.upload(fileName,img_file,'pisight')
    return fileName
