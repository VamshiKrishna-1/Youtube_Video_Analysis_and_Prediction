from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
from fetch_data import Trending
from models import Models
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()


templates = Jinja2Templates(directory= "htmldirectory")


@app.get('/')
def write_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})



@app.post("/submiturl")
async def get_url(request: Request, url: str = Form(...)):
    video_id = Trending.extractVideoId(url)
    if video_id == None:
        return "Enter a valid Youtube video url"
    if Trending.isTrending(video_id):
        input_df = Trending.getInputForPrediction(video_id)
        views_predicted = int(Models.predict_views(input_df))
        likes_predicted = int(Models.predict_likes(input_df))
        comment_count_predicted = int(Models.predict_commentcount(input_df))
        input_df['likes_end_estimate'] = likes_predicted
        input_df['comment_count_estimate'] = comment_count_predicted
        input_df['view_count_estimate'] = views_predicted
        trending_days_predicted = Models.predict_trendingdays(input_df)
        if trending_days_predicted == 1:
            trending_days_predicted = "More than 4 days"
        else:
            info = Trending.getVideoInfo(video_id)
            trending_days_predicted = "Less than 4 days"
            values =  {"Channel Title": info["title"],
                "The video will trend for": trending_days_predicted, 
                "Current number of views": str(input_df["view_count_start"].values[0]), 
                "Predicted views by the time video gets out of trending list":  str(views_predicted), 
                "Current number of likes": str(input_df["likes_start"].values[0]),
                "Predicted Likes by the time video gets out of trending list": str(likes_predicted), 
                "Current number of comment count": str(input_df["comment_count_start"].values[0]),
                "Predicted Comment count by the time video gets out of trending list": str(comment_count_predicted)
                }
        
        return templates.TemplateResponse("values.html", {"request": request, "data": values})
        
        
    else:
        return "The given video is not a trending video"
