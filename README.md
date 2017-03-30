# bballfast 

0. Have pip installed. Use pip to install 1-8.
1. You have `Flask` installed.
2. You have `requests` installed.
3. You install `nba_py`. https://github.com/seemethere/nba_py
4. Install `pytz`.
5. Install `praw`.
6. Install `beautifulsoup4`.
7. Install `google-api-python-client`.
8. Install `python-dateutil`.

To run the server locally.
```
python __init__.py
```

### Create YouTube and Reddit API keys

Put the YouTube and Reddit API keys inside __init__.py.

```
# YouTube Developer Key
DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Reddit API Key
reddit = praw.Reddit(client_id="",
                     client_secret="",
                     user_agent="bballfast by /u/microwavesam")
```
