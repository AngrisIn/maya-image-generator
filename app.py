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

@app.route("/generate")
def generate_image():
	negative_prompt = "character"

	prompt = request.args.get('prompt')
	uuid = request.args.get('uuid')
	scene_number = request.args.get('scene_number')

	print(prompt, negative_prompt, uuid, scene_number)

	if not prompt or not negative_prompt:
		return jsonify({'error': 'Prompt and negative prompt are required'}), 400
	
	engine_id = "stable-diffusion-xl-1024-v1-0"
	api_key = os.getenv('STABILITY_API_KEY')
	api_host = os.getenv('STABILITY_HOST')
	
	headers = {
		'Authorization': f'Bearer {api_key}',
		'Content-Type': 'application/json',
		'Content-Disposition': f'attachment; filename="{uuid}_{scene_number}.png"'
	}
	data={
        "text_prompts": [
            {
                "text": prompt,
				"weight": 1
            },
	    	{
			    "text": negative_prompt,
			    "weight": -1
			}
        ],
		"style": "comic-book",
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30,
    }
	response = requests.post(f"{api_host}/v1/generation/{engine_id}/text-to-image", headers=headers, json=data)

	if response.status_code == 200:
		base64_string = response.json()['artifacts'][0]['base64']
		output_path = base64_to_png(base64_string, f"{uuid}_{scene_number}.png")

		if output_path:
			print(output_path)
			return Response(open(output_path, 'rb').read(), mimetype="image/png")
		else:
			return jsonify({'error': 'Failed to generate image'}), 500
	else:
		return jsonify({'error': 'Failed to generate image'}), 500

if __name__ == '__main__':
	app.run(port=5003)
