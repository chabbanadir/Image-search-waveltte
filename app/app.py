import os
import cv2
import numpy as np


from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename 

from descriptor import DescribeTexture
from ranker import Ranker

UPLOAD_FOLDER = 'static/queries'

# create flask instance
app = Flask(__name__)
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER

INDEX = os.path.join(os.path.dirname(__file__), 'texture.csv')

# main route
@app.route('/')
def index():
    return render_template('index.html', preview="static/init-preview.png")

#rout upload file 
@app.route('/upload',methods= ['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return redirect("/") 

# image database url list route
@app.route('/list', methods=['POST'])
def image_list():

    if request.method == "POST":

        try:

            imgList = [img for img in list(os.listdir(os.path.join(os.path.dirname(__file__), 'static/queries/'))) if img[-4:] in ('.png', '.jpg', '.gif')]

            return jsonify(imgList=imgList)
        
        except Exception as e:
            return jsonify({"sorry": "Sorry, no results! Please try again."}), 500


# search route
@app.route('/search', methods=['POST'])
def search():
 
    if request.method == "POST":

        RESULTS_ARRAY = []

        # get url
        image_url = request.form.get('img')
        print(image_url)
 
        try:
 
            # initialize the image descriptor
            tx = DescribeTexture()
 
            # load the query image and describe it
            from skimage import io
            import cv2

            query = cv2.imread(os.path.join(os.path.dirname(__file__), 'static/queries/'+image_url))
            features = tx.describe_texture(query)

            # perform the search
            searcher = Ranker(INDEX)
            results = searcher.rank(features)
            slice1 = slice(47)
            print(results)
            # loop over the results, displaying the score and image name
            for (score, resultID) in results:
                RESULTS_ARRAY.append(
                    {"image": str(resultID[48:]), "score": str(score)})
                print(RESULTS_ARRAY)
            return jsonify(results=(RESULTS_ARRAY[:101]), preview="images/"+image_url)
 
        except Exception as e:
            print(str(e))
            # return error
            return jsonify({"sorry": "Sorry, no results! Please try again."}), 500

# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
