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


def base64_to_png(base64_data, output_path):
    try:
        # Decode the base64 data into bytes
        png_bytes = base64.b64decode(base64_data)

        # Create a PIL Image object from the bytes data
        image = Image.open(io.BytesIO(png_bytes))

        # Save the image to the specified output path
        image.save(output_path, format="PNG")
        return output_path

    except Exception as e:
        print("Error:", e)
        return None


if __name__ == '__main__':
	app.run()
