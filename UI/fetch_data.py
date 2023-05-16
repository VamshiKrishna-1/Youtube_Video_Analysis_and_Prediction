import pandas as pd
import re
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime
import json



class Trending():
    #api_key = "***********************************"
    api_key = "********************************"
    
    allIds = None

    def __init__(self):
        pass

    def getIdsFromResponse(Response):
        all_ids = []
        for item in Response["items"]:
            all_ids.append(item["id"])
        
        return all_ids


    def getAllIds():

        if Trending.allIds != None:
            return Trending.allIds

        else:
            api_service_name = "youtube"
            api_version = "v3"

            # Get credentials and create an API cl, recordingDetails, snippetient
            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, developerKey= Trending.api_key)

            request = youtube.videos().list(
                part="id",
                chart="mostPopular",
                maxResults = 50
            )
            response = request.execute()

            all_ids = Trending.getIdsFromResponse(response)

            next_page_token = response.get("nextPageToken")

            while next_page_token:
                request = youtube.videos().list(
                    chart="mostPopular",
                    part="id",
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                all_ids.extend(Trending.getIdsFromResponse(response))
                next_page_token = response.get("nextPageToken")

            return all_ids
    
    def isTrending(vid_id):
        if Trending.allIds == None:
            Trending.allIds = Trending.getAllIds()

        if vid_id in Trending.allIds:
            return True
        else:
            return False

    def extractVideoId(url):
        regex = r"(?<=v=)[\w-]+|(?<=be/)[\w-]+"
        match = re.search(regex, url)
        if match:
            return match.group(0)
        else:
            return None
        
    def categoryIDtocategory(category_id):
        # CategoryID
        category_path = '../../youtube-trending-video-dataset/US_category_id.json'

        category_dict = {}

        with open(category_path, 'r') as file:
            json_data = json.load(file)
            for item in json_data['items']:
                category_dict[int(item['id'])] = item['snippet']['title']


        return (category_dict[int(category_id)])
    
    def strToDatetime(datetime_str):
        return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
        
        
    def getVideoInfo(vid_id):
        api_service_name = "youtube"
        api_version = "v3"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=Trending.api_key)

        request = youtube.videos().list(
            part="snippet,contentDetails,statistics,status",
            id=vid_id
        )
        response = request.execute()

        # Extract the desired values from the response
        title = response['items'][0]['snippet']['title']
        published_at = response['items'][0]['snippet']['publishedAt']
        channel_id = response['items'][0]['snippet']['channelId']
        channel_title = response['items'][0]['snippet']['channelTitle']
        category_id = response['items'][0]['snippet']['categoryId']
        description = response['items'][0]['snippet']['description']
        tags = response['items'][0]['snippet']['tags'] if 'tags' in response['items'][0]['snippet'] else []
            
        # Get the current number of views, likes, and comments
        view_count_current = response['items'][0]['statistics']['viewCount']
        like_count_current = response['items'][0]['statistics']['likeCount']
        comment_count_current = response['items'][0]['statistics']['commentCount']

        # Return the extracted values as a dictionary
        return {
            "title": title,
            "published_at": Trending.strToDatetime(published_at),
            "channel_title": channel_title,
            "category_id": Trending.categoryIDtocategory(category_id),
            "description": description,
            "tags": tags,
            "view_count_current": view_count_current,
            "like_count_current": like_count_current,
            "comment_count_current": comment_count_current,
        }
    
    
    def getInputForPrediction(vid_id):
        data = Trending.getVideoInfo(vid_id)

        input_array = []
        
        # channel
        input_array.append(data["channel_title"])
        
        # CategoryID
        input_array.append(data['category_id'])
        
        # Views Count
        input_array.append(int(data["view_count_current"]))
        
        # Likes Count
        input_array.append(int(data["like_count_current"]))
        
        # Comment Count
        input_array.append(int(data["comment_count_current"]))
        
        # comments_disabled
        comments_disabled = False
        if (int(data["comment_count_current"]) > 0):
            comments_disabled = True
        input_array.append(comments_disabled)
        
        # ratings_disabled
        ratings_disabled = False
        if (int(data["like_count_current"]) > 0):
            ratings_disabled = True
        input_array.append(ratings_disabled)
        
        # Year
        input_array.append(data['published_at'].year)
        
        # Month
        input_array.append(data['published_at'].month)
        
        # weeday
        input_array.append(data['published_at'].strftime("%A"))
        
        columns = ['channelTitle', 'categoryId', 'view_count_start', 'likes_start',
       'comment_count_start', 'comments_disabled', 'ratings_disabled', 'Year',
       'Month', 'weekday']
        
        input_df = pd.DataFrame([input_array], columns = columns)
        
        return input_df





