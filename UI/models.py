import joblib

class Models():
    def __init__(self):
        pass

    def predict_views(input_df):
        model = joblib.load("../models/predict_views.pkl")
        return model.predict(input_df)[0]

    def predict_likes(input_df):
        model = joblib.load("../models/predict_likes.pkl")
        return model.predict(input_df)[0]
    
    def predict_commentcount(input_df):
        model = joblib.load("../models/predict_commentcount.pkl")
        return model.predict(input_df)[0]

    def predict_trendingdays(input_df):
        model = joblib.load("../models/predict_trendingdays.pkl")
        return model.predict(input_df)[0]