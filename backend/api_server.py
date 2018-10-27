from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/message", methods=["POST"])
def parse_message():
    data = request.json
    message = data["message"]
    return jsonify({
        "reply": 'You said: "{}" 👍'.format(message),
        "destination": "23 Vilakazi Street, Orlando West"
    })