from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os

app = Flask(__name__)
CORS(app)

# Render pulls your key from the Environment Variables we set up earlier
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTIONS = """
You are a senior Operations Consultant for an Israeli-American non-profit.
Your goal is to help Guy innovate fundraising methods.
1. Always suggest one digital-first fundraising idea.
2. If asked about volunteers, mention the importance of tracking hours.
3. If a query is complex, suggest escalating to a human director.
"""

@app.route('/chat', methods=['POST'])
def chat():
    user_data = request.json
    user_message = user_data.get("message")
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config={'system_instruction': SYSTEM_INSTRUCTIONS},
        contents=user_message
    )
    
    return jsonify({
        "status": "success",
        "reply": response.text
    })

if __name__ == '__main__':
    # Render uses a dynamic port, so we don't hardcode it to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
