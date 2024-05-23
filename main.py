from flask import Flask, request, jsonify
import requests
import base64
import os
from flask_cors import CORS

app = Flask('app')
CORS(app)

API_TOKEN = os.getenv('API_TOKEN')
VISION_TEMPERATURE = os.getenv('VISION_TEMPERATURE')

if API_TOKEN is None:
    raise ValueError("API_TOKEN environment variable is not set.")
if VISION_TEMPERATURE is None:
    raise ValueError("VISION_TEMPERATURE environment variable is not set.")
VISION_TEMPERATURE = float(VISION_TEMPERATURE)

@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'

@app.route('/vision')  # Changed route here
def vision():
    try:
        url = request.args.get('url')
        prompt = request.args.get('prompt')
        if url is None:
            return jsonify({'error': 'URL parameter is missing'}), 400
        
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch image from URL'}), 400
        
        return { "answer": get_pro_llm_response(response.content, prompt) }
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_pro_llm_response(img, prompt):
    try:
        base64_img = base64.b64encode(img).decode("utf-8")

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "inlineData": {
                                "mimeType": "image/jpeg",
                                "data": base64_img
                            }
                        },
                        {
                            "text": prompt
                        },
                    ]
                }
            ],
            "generationConfig": {
                "temperature": VISION_TEMPERATURE,
                "topK": 32,
                "topP": 1,
                "maxOutputTokens": 4096,
                "stopSequences": []
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        headers = {"Content-Type": "application/json"}
        gemini_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key=' + API_TOKEN
        response = requests.post(gemini_url, json=data, headers=headers)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to get response from Gemini API'}), 500
        
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
        
