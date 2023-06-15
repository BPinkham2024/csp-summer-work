from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/chat_log')
def get_chat_log():
    with open('chat_log.json', 'r') as file:
        chat_log = json.load(file)
    return jsonify(chat_log)

if __name__ == '__main__':
    app.run()
