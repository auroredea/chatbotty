#!flask/bin/python
from flask import Flask, request
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import datetime
import time


class TFIDFPredictor:
    _vectorizer = None
    _train_df = None
    _utterances = None

    def __init__(self, data_path):
        self._vectorizer = TfidfVectorizer()
        self._load_data(path=data_path)

    def _load_data(self, path):
        # Load Data
        self._train_df = pd.read_csv(path)
        self._train_df.Label = self._train_df.Label.astype('category')
        self._utterances = self._train_df[self._train_df['Label'] == 1.0]
        self._utterances = np.array(self._utterances['Context'] + "%" + self._utterances['Utterance'])
        # self._utterances = np.array(self._train_df["Utterance"])

    def train(self):
        self._vectorizer.fit(np.append(self._train_df.Context.values, self._train_df.Utterance.values))

    def predict(self, context):
        # Convert context and utterances into tfidf vector
        vector_context = self._vectorizer.transform([context])
        vector_doc = self._vectorizer.transform(self._utterances)
        # The dot product measures the similarity of the resulting vectors
        # result = np.dot(vector_doc, vector_context.T).todense()
        result = vector_doc * vector_context.T
        result = result.todense()
        result = np.asarray(result).flatten()
        result = np.argsort(result, axis=0)[::-1]
        response = str(self._utterances[result[0]])
        # Sort by top results and return the indices in descending order
        return response.split("%")[1]

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
