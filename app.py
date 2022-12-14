from flask import Flask, render_template, request, jsonify
from keras.models import load_model
#from keras.utils import load_img,img_to_array
# from keras.preprocessing import image
from keras.utils import image_utils
import io
import string
import time
import os
import numpy as np
import tensorflow as tf
from PIL import Image


# dic = {0: 'Normal', 1: 'Malignant'}

model = tf.keras.models.load_model('CNN_Cancer.h5')
def prepare_image(img):
    img = Image.open(io.BytesIO(img))
    img = img.resize((224, 224))
    img = np.array(img)
    img = np.expand_dims(img, 0)
    return img

def predict_result(img):
    return 1 if model.predict(img)[0][0] > 0.5 else 0

result='try'
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def infer_image():
    # Catch the image file from a POST request
    if request.method == 'POST':
        file = request.files['my_image']
        result='image readed'

    if not file:
        result=('image not readed')
        return ('not image')

    # Read the image
    img_bytes = file.read()
    result='imgbyte'

    # Prepare the image
    img = prepare_image(img_bytes)
    result='imageprepared'

    # Return on a JSON format
    # return result
    prediction = predict_result(img)
    if prediction == 1 :
        result='Malignant'
    else:
        result='Normal'
#     return result
    return render_template("index.html", result=result)
    
# Create Custom Error Pages
# Invalid Url
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ =='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

