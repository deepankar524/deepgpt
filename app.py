from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient

app = Flask(__name__)

# Initialize Hugging Face InferenceClient
client = InferenceClient(
    provider="novita",
    api_key="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"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    messages = [
        {"role": "user", "content": user_input}
    ]

    response_text = ""
    stream = client.chat.completions.create(
        model="Qwen/Qwen3-235B-A22B",
        messages=messages,
        temperature=0.5,
        max_tokens=500,
        top_p=0.7,
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            response_text += chunk.choices[0].delta.content

    return jsonify({"user_input": user_input, "response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
