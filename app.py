import io
import json                    
import base64                  
import logging             
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input
from flask import Flask, request, jsonify, abort

app = Flask(__name__)          
app.logger.setLevel(logging.DEBUG)
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'space']

@app.route("/test", methods=['POST'])
def test_method():            
    if not request.json or 'image' not in request.json: 
        abort(400)
             
    im_b64 = request.json['image']
    img_file_buffer = base64.b64decode(im_b64.encode('utf-8'))
    image = Image.open(io.BytesIO(img_file_buffer))
    resized_image = image.resize((64, 64))
    input_array = tf.keras.preprocessing.image.img_to_array(resized_image)
    input_array = tf.expand_dims(input_array, axis=0)
    preprocessed_input = preprocess_input(input_array)
    model = tf.keras.models.load_model('Trained_Model.h5')
    predictions = model.predict(preprocessed_input)
    predictions = np.argmax(predictions, axis=1)
    predictions = labels[predictions[0]]
    result_dict = {'output': predictions}
    return result_dict

def run_server_api():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":     
    run_server_api()