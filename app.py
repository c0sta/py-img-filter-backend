from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask import send_file
import cv2
import numpy as np
import matplotlib.pyplot as plt
import io
import os
import pyrebase

app = Flask(__name__)
CORS(app)

config = {
    "apiKey": "AIzaSyCTqzXbhyIXVLI8JzQ4SnlLWGs1v5V-8Y4",
    "authDomain": "image-filter-6d9d4.firebaseapp.com",
    "databaseURL": "https://image-filter-6d9d4.firebaseio.com",
    "projectId": "image-filter-6d9d4",
    "storageBucket": "image-filter-6d9d4.appspot.com",
    "messagingSenderId": "535829169994",
    "appId": "1:535829169994:web:a2ce663674f68e2ebc23b3",
    "measurementId": "G-KF426H3GG1"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
path_on_cloud = 'images/'
path_local = './filtered_images/'


@app.route('/')
def hello_world():
    return 'Hello, world!'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print('###### inside the upload_file! ######')
    if request.method == 'POST':
        file = request.files['file']
        file.save('./images/'+file.filename)
        # print('is fileName correct? ', file.filename)
        extension = file.filename.split('.')[-1]
        filter_image(extension)

        return 'its ok being useless brow'


def filter_image(extension):
    i = 0
    directory = r'./images'  # downloaded images folder
    for entry in os.scandir(directory):  # runs through images folder
        if(extension == 'jpg' or extension == 'png' and entry.is_file()):
            img = cv2.imread(entry.path)
            filtered_filename = 'filtered-image-'+str(i)+'.'+extension
            blurred_img = cv2.GaussianBlur(img, (5, 5), 0)
            cv2.imwrite('./filtered_images/'+filtered_filename, blurred_img)
            storage.child(
                path_on_cloud+filtered_filename).put(path_local+filtered_filename)
            i = i + 1


if __name__ == '__main__':
    app.run()


# todo
# 5 retornar imagem p/ o front || ou só mandar o link do firebase da img

# doing

# done
# 1 - enviar img p/ o back
# 2 - receber img do front
# 3- filtrar a img no back
# 4 - Subir imagens no Firebase
