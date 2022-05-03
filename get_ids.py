from datetime import datetime, timedelta
from dateutil import parser


def get_video_ids(response, days, keyword):
    items = response["items"]
    ids = []
    limit_date = (datetime.now() - timedelta(days=days)).date() if days > -1 else None
    for item in items:
        published_date = parser.parse(item["snippet"]["publishedAt"]).date()
        if (limit_date is None) or (published_date >= limit_date):
            if keyword in item["snippet"]["title"]:
                ids.append(item["snippet"]["resourceId"]["videoId"])

    return ids


def get_playlist_ids(response):
    items = response["items"]
    ids = []
    for item in items:
        channel_id = item["snippet"]["resourceId"]["channelId"]
        ids.append(channel_id.replace("UC", "UU", 1))

    return ids
