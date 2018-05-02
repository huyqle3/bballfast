# bballfast 

[YouTube Tutorial](https://www.youtube.com/watch?v=PLfkns6lZH8)

![bballfast demo image](https://github.com/huyle333/bballfast/blob/master/static/images/demo-1.png)

### Requirements

0. Have `pip` installed. `sudo apt-get install pip`
1. `pip install -r requirements.txt`
2. `OPTIONAL` You can also install the latest version of [nba_py](https://github.com/seemethere/nba_py)

### Create YouTube and Reddit API keys

Create YouTube Data v3 API Credentials Key at:
[https://console.developers.google.com/apis/dashboard](https://console.developers.google.com/apis/dashboard)

Create Reddit Client ID and Client Secret Key at:
[https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)

Put the YouTube and Reddit API keys inside `__init__.py`.

```
# YouTube Developer Key
DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Example Reddit API Key
reddit = praw.Reddit(client_id="gjOCeed5Odsd3a",
                     client_secret="O0GP_rbfgRo_AxW1dyXCjteqGcd",
                     user_agent="bballfast by /u/microwavesam")
```

- If you don't want YouTube functionality, comment out the contents of the YouTube function.

```
def youtube_search(q, max_results=25, freedawkins=None):
    """Searches YouTube for q and returns YouTube link.
    """
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    if (freedawkins):
        search_response = youtube.search().list(q=q,
                                                part="id,snippet",
                                                maxResults=max_results,
                                                channelId="UCEjOSbbaOfgnfRODEEMYlCw").execute()
    else:
        search_response = youtube.search().list(q=q,
                                                part="id,snippet",
                                                maxResults=max_results,
                                                type="video").execute()

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            return "//www.youtube.com/embed/" + search_result["id"]["videoId"]
    """

    return False
```

### Run locally

To run the server locally at [http://127.0.0.1:8080](http://127.0.0.1:8080).
```
python __init__.py
```

![bballfast demo image](https://github.com/huyle333/bballfast/blob/master/static/images/demo-2.png)
