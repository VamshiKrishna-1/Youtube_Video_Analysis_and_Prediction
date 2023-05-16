# Youtube_Video_Analysis_and_Prediction
The objectives of this project are:
1. Analyse the Youtube Trending videos and gain insights on them.
2. Do sentiment analysis on the comments of those videos
3. Predicting the number of trending days given the current state of trending video
4. Predicting the views, likes and comment counts by the time video gets out of the trending list



Required libraries are:
numpy
pandas
sklearn
nltk
matplotlib
seaborn
plotly
xgboost
fastapi[all]


- Link for the Dataset - "https://www.kaggle.com/datasets/rsrishav/youtube-trending-video-dataset?select=US_youtube_trending_data.csv"
- Extracted comments and video duration which were missing in the dataset using Youtube API
- Four Machine Learning models were built (3 Regression models and 1 Classification model)
- Web UI was built using FastAPI