from flask import Flask, request, redirect, url_for, render_template
import os
import json
import glob
from uuid import uuid4
import sys
sys.path.append("../Car_No_Car/")
import MLP as MLP
from PIL import Image
import urllib, cStringIO
import time
sys.path.append("../Image_Description/methods")
import labeling
import capture
from motion_estimation import motion_estimation

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/car_no_car', methods = ['GET', 'POST'])
def car_no_car():
    web_url = request.form['web_url']
    if web_url == "Car.mp4":
        motion_estimation("../Car_No_Car/audi-q7-car-driving-down-neighborhood-street_bfchh41b__PM.mp4")
        mlp = MLP.Image_MLP(img_width = 640, img_height = 480, model_path = "../Car_No_Car/saved_models/cars.h5")
        result = mlp.predict(test_data_dir = "../Car_No_Car/data/test", take_picture = False)
        return result
    elif web_url == "Street.mp4":
        motion_estimation("../Car_No_Car/empty\ street\ video\ background\ royalty\ free\ footage.mp4")
        mlp = MLP.Image_MLP(img_width = 640, img_height = 480, model_path = "../Car_No_Car/saved_models/cars.h5")
        result = mlp.predict(test_data_dir = "../Car_No_Car/data/test", take_picture = False)
        return result
    else:
        mlp = MLP.Image_MLP(img_width = 640, img_height = 480, model_path = "../Car_No_Car/saved_models/cars.h5")
        file = cStringIO.StringIO(urllib.urlopen(web_url).read())
        img = Image.open(file)
        img.save("../Car_No_Car/data/test/test/" + str(int(time.time())) +".jpg")
        result = mlp.predict(test_data_dir = "../Car_No_Car/data/test", take_picture = False)
        print result
        filelist = [ f for f in os.listdir("../Car_No_Car/data/test/test") if (f.endswith(".jpeg") or f.endswith(".jpg")) ]
        for f in filelist:
            os.remove("../Car_No_Car/data/test/test/" + f)
        return result

@app.route('/text', methods = ['GET', 'POST'])
def text():
    web_url = request.form['web_url']
    if web_url == "none":
        fileName = capture.take_photo_and_upload_img()
        text = labeling.detect_text(fileName)
        os.remove("../Image_Description/static/uploads/" + fileName)
        return text
    else:
        return labeling.detect_text_web(web_url)


@app.route('/description', methods = ['GET', 'POST'])
def description():
    web_url = request.form['web_url']
    if web_url == "none":
        fileName = capture.take_photo_and_upload_img()
        description = labeling.get_description(fileName)
        os.remove("../Image_Description/static/uploads/" + fileName)
        return description
    else:
        return labeling.get_description_web(web_url)
