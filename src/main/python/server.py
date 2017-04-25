#!flask/bin/python
from flask import Flask, request
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


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
        self._utterances = np.array(self._train_df["Utterance"])

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
        # Sort by top results and return the indices in descending order
        return self._utterances[result[0]]

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/nlp', methods=['POST'])
def nlp():
    requestBody = request.json

    context = requestBody["context"]
    # question = requestBody["question"]
    response = pred.predict(context)

    return response

if __name__ == '__main__':
    data_path = "/Users/Mouloud/Documents/Xebia/LeMoisDeLaData/2017/nlp/data/ubuntu/train.csv"
    # TFIDF predictor
    pred = TFIDFPredictor(data_path)
    pred.train()
    app.run(debug=True)
