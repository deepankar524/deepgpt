import os
import json
import requests
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the API key from environment variables
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# In-memory chat history
chat_history = []

def query_llama(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",
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
import os
import json
import requests
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the API key from environment variables
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# In-memory chat history
chat_history = []

def query_llama(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",
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