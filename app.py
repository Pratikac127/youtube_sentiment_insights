from flask import Flask, request
import logging
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import os



app = Flask(__name__)
# logging configuration
logger = logging.getLogger('app')
logger.setLevel('DEBUG')

def load_model(model_path: str):
    """Load the trained model."""
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        logger.debug('Model loaded from %s', model_path)
        return model
    except Exception as e:
        logger.error('Error loading model from %s: %s', model_path, e)
        raise

def load_vectorizer(vectorizer_path: str) -> TfidfVectorizer:
    """Load the saved TF-IDF vectorizer."""
    try:
        with open(vectorizer_path, 'rb') as file:
            vectorizer = pickle.load(file)
        logger.debug('TF-IDF vectorizer loaded from %s', vectorizer_path)
        return vectorizer
    except Exception as e:
        logger.error('Error loading vectorizer from %s: %s', vectorizer_path, e)
        raise


@app.route('/')
def home():
    return '''
    <h2>Check sentimaent of comment</h2>
    <form action="/get_sentiment">
        Enter a comment: <input type="string" name="str" required>
        <input type="submit" value="get sentiment">
    </form>
    '''
@app.route('/get_sentiment')
def get_sentiment():
    try:
        result = ""
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        num = str(request.args.get('str'))
        # Load model and vectorizer
        model = load_model(os.path.join(root_dir, 'lgbm_model.pkl'))
        vectorizer = load_vectorizer(os.path.join(root_dir, 'tfidf_vectorizer.pkl'))
        X_test_tfidf = vectorizer.transform([num])
        y_pred = model.predict(X_test_tfidf)

        if y_pred == 1:
            result = "Positive"
        elif y_pred == -1:
            result = "Negative"
        else:
            result = "Neutral"
            

        return f"The sentiment of the comment is '{result}'"

    except Exception as e :
        logger.error("{e}")
        raise

if __name__ == '__main__':
    app.run(host= "0.0.0.0",debug=True)