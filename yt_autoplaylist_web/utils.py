import os
import json

import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime, timedelta
from dateutil import parser

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_client():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    api_key_file = "../credentials/api_key.json"
    # Get API key
    with open(api_key_file, "r") as f:
        developer_key = json.load(f)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_key["api_key"])

    return youtube


def get_videos_from_playlist(youtube, playlist_id, max_results):
    try:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=max_results
        )
        response = request.execute()

        return response

    except Exception:
        pass


def get_video_ids(response, days, keyword):
    items = response["items"]
    ids = []
    limit_date = (datetime.now() - timedelta(days=days)).date() if days > -1 else None
    for item in items:
        published_date = parser.parse(item["snippet"]["publishedAt"]).date()
        if (limit_date is None) or (published_date >= limit_date):
            if keyword in item["snippet"]["title"]:
                print(item)
                ids.append(item["snippet"]["resourceId"]["videoId"])

    return ids


def get_playlist_ids(response):
    items = response["items"]
    ids = []
    for item in items:
        channel_id = item["snippet"]["resourceId"]["channelId"]
        ids.append(channel_id.replace("UC", "UU", 1))

    return ids
