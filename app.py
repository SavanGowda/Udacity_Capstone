import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from keras.models import load_model
from keras import backend as K

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
	"""allowed files"""
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
	"""This method gives the input to the ML Model and gets the Predictions"""
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			image = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + "/uploads/" + filename)
			color_result = get_dominant_color(image)
			result = cat_or_dog(image)
			redirect(url_for('upload_file', filename=filename))
			return '''
				<!DOCTYPE html>
					<title> Savan's AI Results </title>
					<style>
						input[type=file], select {
							width: 100%;
							padding: 12px 20px;
							margin: 8px 0;
							display: inline-block;
							border: 1px solid #ccc;
							border-radius: 4px;
							box-sizing: border-box;
						}
					</style>
					<div style="text-align:center;border:5px dashed white;background-color:blue;">
						<p></p>
						<p style="color:white;font-size:40px;">Savan's Cat and Dog Machine Learning Blue Model... Enjoy! :)</p>
						<p></p>
					</div>
					<div style="text-align:center;border:5px dashed black;background-color:white;">
						<p style="color:black;font-size:20px"> Upload another pic of a Cat or a Dog </p>
						<form method=post enctype=multipart/form-data>
							<input type=file name=file>
							<input type=submit value=Upload>
						</form>
					</div>
					<div style="text-align:center;border:5px dashed #D9D61F;background-color:white;">
						<p style="color:green;font-size:25px">The image contains a - '''+result+'''</p>
						<p style="color:green;font-size:25px">The dominant color in the image is - '''+color_result+'''</p>
					</div>
				'''
	return '''
		<!doctype html>
			<title>Savan's AI Homepage</title>
			<style>
				input[type=file], select {
					width: 100%;
					padding: 12px 20px;
					margin: 8px 0;
					display: inline-block;
					border: 1px solid #ccc;
					border-radius: 4px;
					box-sizing: border-box;
				}
			</style>
			<div style="text-align:center;border:5px dashed white;background-color:blue;">
				<p></p>
				<p style="color:white;font-size:40px;">Savan's Cat and Dog Machine Learning Blue Model... Enjoy! :)</p>
				<p></p>
			</div>
			<div style="text-align:center;border:5px dashed black;background-color:white;">
				<p style="color:black;font-size:20px"> Upload any pic of a Cat or a Dog </p>
				<form method=post enctype=multipart/form-data>
					<input type=file name=file>
					<input type=submit value=Upload>
				</form>
				<p></p>
			</div>
		'''


def cat_or_dog(image):
	""" Determines if the image contains a cat or dog"""
	classifier = load_model('./models/cats_vs_dogs_V1.h5')
	image = cv2.resize(image, (150, 150), interpolation=cv2.INTER_AREA)
	image = image.reshape(1, 150, 150, 3)
	res = str(classifier.predict_classes(image, 1, verbose=0)[0][0])
	print(res)
	print(type(res))
	if res == "0":
		res = "Cat"
	else:
		res = "Dog"
	K.clear_session()
	return res


def get_dominant_color(image):
	"""returns the dominate color among Blue, Green and Reds in the image"""
	blue, green, red = cv2.split(image)
	blue, green, red = np.sum(blue), np.sum(green), np.sum(red)
	color_sums = [blue, green, red]
	color_values = {"0": "Blue", "1":"Green", "2": "Red"}
	return color_values[str(np.argmax(color_sums))]


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)
