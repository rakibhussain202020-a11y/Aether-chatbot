import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic

app = Flask(__name__)
CORS(app)

# Render Environment variable se API key lega (secure)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json.get('message', '')
    try:
        m = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system="You are Aether, a friendly AI assistant. Reply in Hinglish.",
            messages=[{"role": "user", "content": msg}]
        )
        return jsonify({"reply": m.content[0].text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
