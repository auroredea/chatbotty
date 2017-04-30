#!flask/bin/python
from flask import Flask, request
import sys
import datetime
from TFIDFPredictor import TFIDFPredictor


app = Flask(__name__)

@app.route('/rnn', methods=['POST'])
def rnn():
    requestBody = request.json

    context = requestBody["context"]
    question = requestBody["question"]

    return "RNN TODO with " + context + " and " + question

@app.route('/tfidf', methods=['POST'])
def tfidf():
    requestBody = request.json

    context = requestBody["context"]
    # question = requestBody["question"]
    before = datetime.datetime.now()
    response = model.predict(context)
    after = datetime.datetime.now()
    delta = after - before
    print("Response time :" + str(delta))
    return response

if __name__ == '__main__':
    data_path = sys.argv[1]
    print("Data Path is :" + data_path)
    print("Loading Data...")
    # TFIDF predictor
    model = TFIDFPredictor(data_path)
    print("Loading Data succeeded")
    print("Training TFIDF Model...")
    model.train()
    print("Training TFIDF Model succeeded")
    app.run(debug=False, use_reloader=False)
