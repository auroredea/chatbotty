import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cluster
from sklearn.pipeline import make_pipeline
from sklearn.externals import joblib


class TFIDFPredictor:
    _vectorizer = None
    _kmeans = None
    _train_df = None
    _utterances = None
    _pipelinemodel= None

    def __init__(self, data_path):
        self._vectorizer = TfidfVectorizer()
        self._load_data(path=data_path)

    def _load_data(self, path):
        # Load Data
        self._train_df = pd.read_csv(path)
        self._train_df.Label = self._train_df.Label.astype('category')

    def train(self):
        self._vectorizer.fit(np.append(self._train_df.Context.values, self._train_df.Utterance.values))
        self._utterances = self._train_df[self._train_df['Label'] == 1.0].reset_index()
        self._pipelinemodel = joblib.load('../../../model/kmeans_pipeline.pkl')
        context_clust = self._pipelinemodel.predict(self._utterances.Context.values)
        context_clust = pd.DataFrame(context_clust, columns=["cluster"])
        self._utterances = pd.concat([self._utterances, context_clust], axis=1)


    def predict(self, context):
        # Convert context and utterances into tfidf vector
        vector_context = self._vectorizer.transform([context])

        # get the context's cluster
        context_cluster = float(self._pipelinemodel.predict([context])[0])
        print("cluster : " + str(context_cluster))

        # get utterances from the cluster
        utterances = self._utterances[self._utterances["cluster"] == context_cluster].reset_index()
        utterances = np.array(utterances['Context'] + "%" + utterances['Utterance'])
        vector_doc = self._vectorizer.transform(utterances)
        # The dot product measures the similarity of the resulting vectors
        # result = np.dot(vector_doc, vector_context.T).todense()
        result = vector_doc * vector_context.T
        result = result.todense()
        result = np.asarray(result).flatten()
        result = np.argsort(result, axis=0)[::-1]
        response = str(utterances[result[0]])
        # Sort by top results and return the indices in descending order
        return response.split("%")[1]