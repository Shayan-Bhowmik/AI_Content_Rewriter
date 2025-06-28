from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route('/rewrite', methods=['POST'])
def rewrite_content():
    data = request.get_json()
    input_text = data.get('text')
    target_tone = data.get('tone', 'neutral')

    if not input_text:
        return jsonify({"error": "No input text provided."}), 400

    prompt = f"Rewrite the following content in a {target_tone} tone while preserving meaning and factual accuracy:\n\n{input_text}"

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        body = {
            "model": "mistralai/mixtral-8x7b-instruct",  
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

        if response.status_code != 200:
            print("OpenRouter API error:", response.text)
            return jsonify({"error": response.text}), 500

        result = response.json()
        rewritten_text = result["choices"][0]["message"]["content"].strip()
        return jsonify({"rewritten": rewritten_text})

    except Exception as e:
        print("Exception occurred:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
