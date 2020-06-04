from flask import Flask, flash, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from flask import send_file
import cv2
import numpy as np
import io
import os
import pyrebase

app = Flask(__name__) 
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

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
def clean_images_folder(folder):
    filelist = [f for f in os.listdir(
        folder) if f.endswith(".png") or f.endswith(".jpg")]

    for file in filelist:
        os.remove(os.path.join(folder, file))


def blur_img(img, size):
    return cv2.GaussianBlur(img, (size, size), cv2.BORDER_DEFAULT)


def to_gray_img(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def filter_image(extension, name, filter_type):
    i = 0
    directory = r'./images'  # downloaded images folder
    for entry in os.scandir(directory):  # runs through images folder
        if(extension == 'jpg' or extension == 'png' and entry.is_file()):
            img = cv2.imread(entry.path)
            
            if(filter_type == 'gray'):
                gray_img = to_gray_img(img)
                cv2.imwrite('./filtered_images/'+name, gray_img)
            elif(filter_type == 'blur'):
                blurred_img = blur_img(img, 5)
                cv2.imwrite('./filtered_images/'+name, blurred_img)
                
            url = storage.child(path_on_cloud+name).get_url('f166a7c9-2b95-4008-99e7-22cb66444d6a')
            # store filtered images in the firebase storage
            storage.child(
                path_on_cloud+name).put(path_local+name)
            i = i + 1
            return url
        else:
            return "Tipo errado de arquivo"


"""
ROUTES
"""
@app.route('/')
def main_route():
    return jsonify(
        message = "Use a rota /upload para subir as imagens!"
    )


@app.route('/upload/<filter_type>', methods=['GET', 'POST'])
def upload_file(filter_type):
    print('###### inside the upload_file! ######')
    if request.method == 'POST':
        file = request.files['file']
        file.save('./images/'+file.filename)
        # print('is fileName correct? ', file.filename)
        extension = file.filename.split('.')[-1]
        url = filter_image(extension, file.filename, filter_type)
        # clean images folder
        clean_images_folder('./filtered_images/')
        clean_images_folder('./images/')
        return jsonify(url=url)
    if request.method == 'GET':
        return jsonify(message='Rota utilizada para fazer upload de imagens')

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
