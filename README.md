# YouTube Auto-Playlist
Create personalized YouTube playlists from your subscriptions feed based on your preferences, using the following parameters:
* Keyword in video title (e g. titles that contain the word "music"
* How old the video is (e g. videos uploaded in the last 2 days)
* Number of videos looked up per channel (e g. look up the last 10 videos from each channel)

## Table of contents
* [Setup](#setup)
* [Usage](#usage)
* [Technologies](#technologies)

## Setup
1. Download and extract .ZIP

2. You need your own authorization credentials from Google to use the YouTube API. Follow this guide: 
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
When you run the command for the first time, a browser window will be opened and you will be asked to authorize the app.

You can use the help command to learn more about the command's usage and syntax:
```
python -m autoplaylist --help
``` 

## Technologies
### This project was designed with:
* Python 3

#### Dependencies:
<p><img src="https://avatars.githubusercontent.com/u/16785467?s=40&v=4" height="16px"></img> googleapis / google-api-python-client (~> 2.46.0)</p>
<p><img src="https://avatars.githubusercontent.com/u/16785467?s=40&v=4" height="16px"></img> googleapis / oauth2client (4.1.3)</p>
<p><img src="https://avatars.githubusercontent.com/u/17128733?s=40&v=4" height="16px"></img> httplib2 / httplib2 (~> 2.46.0)</p>
<p><img src="https://avatars.githubusercontent.com/u/9849410?s=40&v=4" height="16px"></img> dateutil / dateutil python-dateutil (~> 2.8.2)</p>
