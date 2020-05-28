from flask import Flask, flash, request, redirect, url_for, session
from flask_cors import CORS
from flask import send_file
import cv2
import numpy as np
import io
import os
import pyrebase

app = Flask(__name__)
CORS(app)

"""
FIREBASE CONFIGURATION
"""
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


"""
METHODS
"""


def blur_img(img, size):
    return cv2.GaussianBlur(img, (size, size), 0)


def to_gray_img(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def filter_image(extension, name):
    i = 0
    directory = r'./images'  # downloaded images folder
    for entry in os.scandir(directory):  # runs through images folder
        if(extension == 'jpg' or extension == 'png' and entry.is_file()):
            img = cv2.imread(entry.path)
            blurred_img = blur_img(img, 5)
            # gray_img = to_gray_img(img)
            cv2.imwrite('./filtered_images/'+name, blurred_img)
            # cv2.imwrite('./filtered_images/'+name, gray_img)
            storage.child(
                path_on_cloud+name).put(path_local+name)
            i = i + 1


def clean_images_folder(folder):
    filelist = [f for f in os.listdir(
        folder) if f.endswith(".png") or f.endswith(".jpg")]

    for file in filelist:
        os.remove(os.path.join(folder, file))


"""
ROUTES
"""


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print('###### inside the upload_file! ######')
    if request.method == 'POST':
        file = request.files['file']
        file.save('./images/'+file.filename)
        # print('is fileName correct? ', file.filename)
        extension = file.filename.split('.')[-1]
        filter_image(extension, file.filename)
        # clean images folder
        clean_images_folder('./filtered_images/')
        clean_images_folder('./images/')
        return {"message": "Success"}
    else: 
        return {"message": "Everything cool here :)"}


"""
MAIN
"""
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
