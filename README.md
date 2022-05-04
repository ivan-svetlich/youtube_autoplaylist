# YouTube Auto-Playlist
Create personalized YouTube playlists from your subscriptions feed based on your preferences, using the following parameters:
* Keyword in video title (e g. titles that contain the word "music")
* How old the video is (e g. videos uploaded in the last 2 days)
* Number of videos looked up per channel (e g. look up the last 10 videos from each channel)

## Table of contents
* [Setup](#setup)
* [Usage](#usage)
* [Technologies](#technologies)

## Setup
1. Download and extract .ZIP

2. You need your own authorization credentials from Google to use the YouTube API. Follow this guide to register an app in Google Cloud Platform: 
* https://developers.google.com/youtube/registering_an_application 

3. Open the project's folder, then credentials. Insert your API keys and OAuth 2.0 client secrets in the corresponding files.

4. You need to have python and pip installed on your computer to run this code:
  * Python: https://docs.python-guide.org/starting/installation/
  * pip: https://pip.pypa.io/en/stable/installation/

5. Open a terminal/command prompt, cd to the folder containing the autoplaylist.py file and run:
```
pip install -r requirements.txt
```
## Usage
To create a playlist run:
```
python -m autoplaylist -d [DAYS] -k [KEYWORD] -r [RESULTS_PER_CHANNEL]
```
or
```
python -m autoplaylist --days [DAYS] --keyword [KEYWORD] --results [RESULTS_PER_CHANNEL]
```
When you run the command for the first time, a browser window will be opened and you will be asked to authorize the app. Make sure your Google account is added to the 'Test Users' list in the Google Cloud Platform console.

A YouTube playlist titled "[KEYWORD] Auto Playlist ([CURRENT DATETIME])", containing the videos that matched your preferences, is created in your library.

You can use the help command to learn more about the command's usage and syntax:
```
python -m autoplaylist --help
```

## Example
Let's run the command using the default preferences:
```
python -m autoplaylist --days 0 --keyword 歌 --results 2
```
This command will search the last 2 uploads from each channel. looking for videos uploaded today that contain the word "歌" (song in Japanese). Because these are the default values, you can get the same result by simply running:
```
python -m autoplaylist
```
Feel free to modify the code to set different default values. 

If it's the first run, we need to complete the OAuth2 authorization. Bacause the app status is set to "Testing" in Google Cloud Platform, we'll see the following warning:

<p align="center"><img alt="warning" src="https://github.com/ivan-svetlich/youtube_autoplaylist/blob/master/images/autoplaylist_oauth_1.png"</p>

After we click continue, we get the usual authorization screen:

 <p align="center"><img alt="authorization" src="https://github.com/ivan-svetlich/youtube_autoplaylist/blob/master/images/autoplaylist_oauth_2.png"</p>

This step won't be necesary next time you run the command. If you want to use a different Google account, just delete the ```autoplaylist.py-oauth2.json``` file and you'll be asked for authorization again.

If everything goes well, we should see an output like this:
```
Authenticating....
...
Authentication successful.
Searching playlists...
Done. 159 playlists found.
Searching videos...
Done. 8 videos found.
Creating new playlist...
Done. New playlist: 歌 Auto Playlist (2022-05-03 10:00:30.668473)
Adding videos to playlist...
Done. 8 videos added to playlist.
```

And we should find the new playlist in our YouTube library:

 <p align="center"><img alt="playlist" src="https://github.com/ivan-svetlich/youtube_autoplaylist/blob/master/images/autoplaylist_result.png"</p>

## Technologies
### This project was designed with:
* Python 3

#### Dependencies:
<p><img src="https://avatars.githubusercontent.com/u/16785467?s=40&v=4" height="16px"></img> googleapis / google-api-python-client (~> 2.46.0)</p>
<p><img src="https://avatars.githubusercontent.com/u/16785467?s=40&v=4" height="16px"></img> googleapis / oauth2client (4.1.3)</p>
<p><img src="https://avatars.githubusercontent.com/u/17128733?s=40&v=4" height="16px"></img> httplib2 / httplib2 (~> 2.46.0)</p>
<p><img src="https://avatars.githubusercontent.com/u/9849410?s=40&v=4" height="16px"></img> dateutil / dateutil python-dateutil (~> 2.8.2)</p>
