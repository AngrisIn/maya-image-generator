from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import base64
import io
from PIL import Image

app = Flask(__name__)
CORS(app)
load_dotenv()

@app.route('/')
def hello_world():
	return "PONG"



if __name__ == '__main__':
	app.run()
