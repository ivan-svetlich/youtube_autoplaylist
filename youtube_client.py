#!/usr/bin/python
import sys
import warnings

import httplib2
import os
import traceback

from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from google.auth.exceptions import MutualTLSChannelError


class YoutubeClient:
    CLIENT_SECRETS_FILE = "credentials/client_secrets.json"

    # This variable defines a message to display if the CLIENT_SECRETS_FILE is
    # missing.
    MISSING_CLIENT_SECRETS_MESSAGE = """
    WARNING: Please configure OAuth 2.0

    To make this sample run you will need to populate the client_secrets.json file
    found at:

       %s

    with information from the API Console
    https://console.developers.google.com/

    For more information about the client_secrets.json file format, please visit:
    https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    """ % os.path.abspath(os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE))

    # This OAuth 2.0 access scope allows for full read/write access to the
    # authenticated user's account.
    YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    def __init__(self) -> None:
        flow = flow_from_clientsecrets(self.CLIENT_SECRETS_FILE,
                                       scope=self.YOUTUBE_READ_WRITE_SCOPE,
                                       message=self.MISSING_CLIENT_SECRETS_MESSAGE)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            storage = Storage(f"{sys.argv[0]}-oauth2.json")
            credentials = storage.get()

        if credentials is None or credentials.invalid:
            try:
                flags = argparser.parse_args(args=[])
                credentials = run_flow(flow, storage, flags)
            except Exception:
                traceback.print_exc()
        else:
            print("Authentication successful.")

        try:
            self.youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                                 http=credentials.authorize(httplib2.Http()))
        except MutualTLSChannelError:
            traceback.print_exc()

    def get_subscriptions(self):
        responses = []
        request = self.youtube.subscriptions().list(
            part="snippet",
            maxResults=20,
            mine=True,
        )
        response = request.execute()
        responses.append(response)

        while "nextPageToken" in response:
            request = self.youtube.subscriptions().list(
                part="snippet",
                maxResults=20,
                mine=True,
                pageToken=response["nextPageToken"]
            )
            response = request.execute()
            responses.append(response)

        return responses

    def create_playlist(self, title):
        try:
            playlists_insert_response = self.youtube.playlists().insert(
                part="snippet,status",
                body=dict(
                    snippet=dict(
                        title=title,
                        description="Auto Playlist"
                    ),
                    status=dict(
                        privacyStatus="private"
                    )
                )
            ).execute()

            return playlists_insert_response["id"]

        except Exception:
            traceback.print_exc()

    def add_video_to_playlist(self, playlist_id, video_id):
        try:
            request = self.youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            response = request.execute()

            return response

        except Exception:
            traceback.print_exc()
