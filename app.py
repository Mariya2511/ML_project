import dill
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type
#import cloudpickle
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

app = Flask(__name__)
model = None


handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		model = dill.load(f)
	print(model)
	return model

modelpath = "my_project/my_flask_app/pipeline.dill"
load_model(modelpath)
@app.route("/", methods=["GET"])
def general():
	return """Welcome to prediction process. Please use 'http://<address>/predict' to POST"""

@app.route("/predict", methods=["GET", "POST"])


def predict():
	import flask
	data = {"success": False, "predictions": ''}
	print(data)
	comment = "and change around both files to figure out what is sending the issue, I feel like it is something simple, but if you can help me, I bet this will help me and many others that are"
	print(comment)
	if (flask.request.method == "POST"):
		request_json = flask.request.get_json()
		print(request_json)
		if request_json["comment"]:
			comment = request_json["comment"]
		logger.info(f'Data: comment={comment}')
		try:
			preds = model.predict_proba(pd.DataFrame({"comment": [comment]}))
		except AttributeError as e:
			logger.warning(f'Exception: {str(e)}')
			data['predictions'] = str(e)
			data['success'] = False
			return data

		data["predictions"] = preds[:, 1][0]
		# indicate that the request was a success
		data["success"] = True
		print(data)
	# return the data dictionary as a JSON response
	return flask.jsonify(data)


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')