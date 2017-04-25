#!flask/bin/python
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/nlp', methods=['POST'])
def nlp():
    requestBody = request.json

    context = requestBody["context"]
    question = requestBody["question"]

    return "Calling python through scala with context = '" + context + "' and question = " + question

if __name__ == '__main__':
    app.run(debug=True)