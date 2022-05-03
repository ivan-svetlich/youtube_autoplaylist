import os
import json

import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_videos_from_playlist(playlist_id, max_results):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    api_key_file = "credentials/api_key.json"
    # Get API key
    with open(api_key_file, "r") as f:
        developer_key = json.load(f)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_key["api_key"])

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
