# -*- coding: utf-8 -*-
import os
from datetime import datetime

import flask
from flask_cors import CORS, cross_origin
from flask import request

import google.oauth2.credentials
from google_auth_oauthlib.flow import Flow
from utils import get_playlist_ids, get_video_ids, get_client, get_videos_from_playlist
from youtube_client import YoutubeClient

CLIENT_SECRETS_FILE = "../credentials/client_secrets.json"
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

app = flask.Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
CORS(app, support_credentials=True)


@app.route('/')
@cross_origin(supports_credentials=True)
def index():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load the credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    if credentials is None or credentials.expired or not credentials.valid:
        return flask.redirect('authorize')

    keyword = request.args.get("keyword")
    days = int(request.args.get("days"))
    results_per_channel = int(request.args.get("max_results"))

    print("Authenticating....")

    youtube_client = YoutubeClient(credentials)

    print("Searching playlists...")

    subs_responses = youtube_client.get_subscriptions()
    playlist_ids = []
    video_ids = []
    for sub_response in subs_responses:
        playlist_ids.extend(get_playlist_ids(sub_response))

    num_playlists = len(playlist_ids)

    print(f"Done. {num_playlists} playlist{'s' if num_playlists != 1 else ''} found.")
    print("Searching videos...")

    api_client = get_client()
    for playlist_id in playlist_ids:
        videos_response = get_videos_from_playlist(youtube=api_client, playlist_id=playlist_id,
                                                   max_results=results_per_channel)
        if videos_response is not None:
            ids = get_video_ids(videos_response, days, keyword)
            video_ids.extend(ids)

    num_videos = len(video_ids)

    print(f"Done. {num_videos} video{'s' if num_videos != 1 else ''} found.")

    if num_videos > 0:
        print(f"Creating new playlist...")

        playlist_title = f"{keyword} Auto Playlist ({datetime.now()})"
        playlist_id = youtube_client.create_playlist(playlist_title)

        print(f"Done. New playlist: {playlist_title}")
        print(f"Adding videos to playlist...")

        for video_id in video_ids:
            youtube_client.add_video_to_playlist(playlist_id, video_id)

        print(f"Done. {num_videos} video{'s' if num_videos != 1 else ''} added to playlist.")
    else:
        print("Try increasing the number of results per channel "
              "and/or the number of days for the search")
        print("Use --help command to get info about the optional arguments.")

    return flask.redirect("http://localhost:3000/success")


@app.route('/authorize')
@cross_origin(supports_credentials=True)
def authorize():
    # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        # This parameter enables offline access which gives your application
        # both an access and refresh token.
        access_type='offline',
        # This parameter enables incremental auth.
        include_granted_scopes='true')

    # Store the state in the session so that the callback can verify that
    # the authorization server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verify the authorization server response.
    state = flask.session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.
    credentials = flow.credentials
    flask.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return flask.redirect(flask.url_for('index'))
