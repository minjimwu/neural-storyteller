import os
import argparse
from flask import Flask, request, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
import random
import string
import json

from datetime import datetime

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024 #1GB
app.debug = True

import generate
z = generate.load_all()
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':      
        
        # check if the post request has the file part
        if 'file' not in request.files:         
            return jsonify({'result': False, 'message': 'no file'})
              
        file = request.files['file']
        
        if file.filename == '':            
            return jsonify({'result': False, 'message': 'no file name'})

        if file:
            filename = secure_filename(file.filename)

            # get randome key            
            target_folder = UPLOAD_FOLDER
            
            # create folder if not existed
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            
            # save file
            file_path = os.path.join(target_folder, file.filename)
            file.save(file_path)

            story = get_story(file_path)
            return jsonify({'story': story})

def get_story(file_path):
    #return 'test'
    return generate.story(z, file_path)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()    
    parser.add_argument("-p", "--port", help="port", type=int, required=False, default=5000)
    parser.add_argument("-s", "--server", help="host", type=str, required=False, default='0.0.0.0')    
    
    args = parser.parse_args()       
    
    app.run(host=args.server, port=args.port)        
