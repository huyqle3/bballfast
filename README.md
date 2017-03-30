# bballfast 

[YouTube tutorial](https://www.youtube.com/watch?v=PLfkns6lZH8)

### Requirements

0. Have `pip` installed. Use `pip install package` to install 1-8.
1. You have `Flask` installed.
2. You have `requests` installed.
3. You install `nba_py`. https://github.com/seemethere/nba_py
4. Install `pytz`.
5. Install `praw`.
6. Install `beautifulsoup4`.
7. Install `google-api-python-client`.
8. Install `python-dateutil`.

### Create YouTube and Reddit API keys

Put the YouTube and Reddit API keys inside __init__.py.

Create YouTube Data v3 API Credentials Key at:
[https://console.developers.google.com/apis/dashboard](https://console.developers.google.com/apis/dashboard)

Create Reddit Client ID and Client Secret Key at:
[https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)

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

### Setup locally

To run the server locally at [http://127.0.0.1:8080](http://127.0.0.1:8080).
```
python __init__.py
```
