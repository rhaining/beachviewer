from flask import Flask, request
from beach_handler import BeachHandler
import os

app = Flask(__name__, template_folder=os.environ.get("TEMPLATES_DIR"))
beach_host = "beach.haining.ws"
localhost = beach_host

@app.route('/')
def slash():
	if request.headers['Host'] is beach_host or (request.headers['Host'] == "localhost:5000" and beach_host == localhost):
		return BeachHandler().get(request)
	else:
		return "tbd"

@app.route('/static/<path:path>')
def send_static(path):
	return send_from_directory('static', path)

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
