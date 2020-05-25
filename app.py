from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS
import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow
%matplotlib inline

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, world!'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print('in the upload_file!')
    if request.method == 'POST':
        f = request.files['file']
        print('INFERNOOO', request.files)
        f.save('./images/'+f.filename)
        return 'file uploaded successfully!'


if __name__ == '__main__':
    app.run()
