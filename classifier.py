import joblib
import pickle


class Classifier(object):
    def __init__(self):
        self.vectorizer = joblib.load("vectorizer_dump.pkl")
        self.models = joblib.load("models_dump.pkl")
        self.genres = joblib.load("genres_dump.pkl")

    def predict_text(self, text):
        try:
            result = [];
            vectorized = self.vectorizer.transform([text])
            for index, model in enumerate(self.models):
              prediction = model.predict_proba(vectorized)
              if (prediction[0][1] > 0.28):
                  result.append(self.genres[index])
            return ", ".join(result)
        except:
            print("prediction error")
            return None

    def get_result_message(self, text):
        return self.predict_text(text)
