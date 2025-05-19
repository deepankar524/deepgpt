import os
import json
import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# ✅ Hardcoded API Key (NOT recommended for production)
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

chat_history = []

def query_llama(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-4",  # 🔄 or use a model you're allowed to access
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.7
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "No response from model.")
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", chat_history=chat_history)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("user_input", "")
    if user_input:
        response = query_llama(user_input)
        chat_history.append({"user_input": user_input, "response": response})
        return jsonify({"user_input": user_input, "response": response})
    return jsonify({"error": "No input provided."}), 400

if __name__ == "__main__":
    app.run(debug=True)
