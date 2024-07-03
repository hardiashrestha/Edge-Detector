from flask import Flask, request, render_template, send_file
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

app = Flask(__name__)

# Directory to save uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        # Process the image
        img = cv2.imread(file_path)
        edges = cv2.Canny(img, 100, 200)

        # Save the edge detected image
        edges_path = os.path.join(UPLOAD_FOLDER, 'edges_' + file.filename)
        cv2.imwrite(edges_path, edges)

        return send_file(edges_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
