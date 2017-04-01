from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from bballfast_constants import TEAM_NAME_TO_ID
from bballfast_constants import TEAM_ID_TO_NAME
from bballfast_constants import TEAM_ID_DATA
from bballfast_constants import CITY_TO_TEAM

import nba_py
from nba_py.constants import CURRENT_SEASON
from nba_py.constants import TEAMS
from nba_py import constants
from nba_py import game
from nba_py import player
from nba_py import team
from nba_py import league
from nba_py import draftcombine

import praw

import collections
import datetime
import dateutil.parser
import pytz
import requests
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from bs4 import BeautifulSoup

# YouTube Developer Key
DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

app = Flask(__name__)

# Time zone that determines when the next day occurs.
hawaii = pytz.timezone("US/Hawaii")

# Reddit API Key
reddit = praw.Reddit(client_id="",
                     client_secret="",
                     user_agent="bballfast by /u/microwavesam")

"""
# A function that forces recaching every 10 minutes.
@app.after_request
def add_header(response):
    # Add headers to both force latest IE rendering engine or Chrome Frame,
    # and also to cache the rendered page for 10 minutes.
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
"""

@app.route('/')
def index():
    """Main page of the website that by default renders the score page.
    """
    datetime_today = datetime.datetime.now(hawaii)
    datestring_today = datetime_today.strftime("%m-%d-%Y")

    return render_score_page("index.html", datestring_today, "bballfast.com")

@app.route('/standings')
def standings():
    """Default standings page.
    """
    scoreboard = nba_py.Scoreboard()
    east_standings = scoreboard.east_conf_standings_by_day()
    west_standings = scoreboard.west_conf_standings_by_day()

    return render_template("standings.html",
                           title="standings",
                           east_standings=enumerate(east_standings, 1),
                           west_standings=enumerate(west_standings, 1),
                           team=CITY_TO_TEAM)

@app.route('/standings/season/<season>')
def standings_by_season(season):
    """Standings page by the season year.
    """
    season = int(season) + 1
    scoreboard = nba_py.Scoreboard(month=7,
                                   day=1,
                                   year=season)
    east_standings = scoreboard.east_conf_standings_by_day()
    west_standings = scoreboard.west_conf_standings_by_day()

    return render_template("standings.html",
                           title="standings",
                           east_standings=enumerate(east_standings, 1),
                           west_standings=enumerate(west_standings, 1),
                           team=CITY_TO_TEAM)

@app.route('/standings', methods=["POST"])
def standings_post_request():
    """Standings page after using the datepicker plugin.
    """
    date = request.form["date"]
    datetime_object = datetime.datetime.strptime(date, "%m-%d-%Y")

    scoreboard = nba_py.Scoreboard(month=datetime_object.month,
                                   day=datetime_object.day,
                                   year=datetime_object.year)
    east_standings = scoreboard.east_conf_standings_by_day()
    west_standings = scoreboard.west_conf_standings_by_day()

    return render_template("standings.html",
                           title="standings",
                           east_standings=enumerate(east_standings, 1),
                           west_standings=enumerate(west_standings, 1),
                           team=CITY_TO_TEAM)
    

@app.route('/scores/<datestring>')
def scores(datestring):
    """Link for specific score pages for a certain day.
    """
    return render_score_page("scores.html", datestring, datestring)

@app.route('/scores', methods=["POST"])
def scores_post_request():
    """The score page after using the datepicker plugin.
    """
    date = request.form["date"]
    print(date)
    return render_score_page("scores.html", date, date)

def render_score_page(page, datestring, title):
    """
    Args:
        page: Name of the template html page.
        datestring: The date of the boxscores that we want.
    """
    datetime_today = dateutil.parser.parse(datestring)
    pretty_today = datetime_today.strftime("%b %d, %Y")
    datetime_yesterday = datetime_today - datetime.timedelta(1)
    datetime_tomorrow = datetime_today + datetime.timedelta(1)
    datestring_yesterday = datetime_yesterday.strftime("%m-%d-%Y")
    pretty_yesterday = datetime_yesterday.strftime("%b %d, %Y")
    datestring_tomorrow = datetime_tomorrow.strftime("%m-%d-%Y")
    pretty_tomorrow = datetime_tomorrow.strftime("%b %d, %Y")

    return_tuple = get_games(datetime_today)
    games = return_tuple[0]
    east_standings = return_tuple[1]
    west_standings = return_tuple[2]

    winners = []
    for i in games:
        if (i["HOME_TEAM_PTS"] > i["AWAY_TEAM_PTS"]):
            winners.append(i["HOME_TEAM"])
        elif (i["HOME_TEAM_PTS"] < i["AWAY_TEAM_PTS"]):
            winners.append(i["AWAY_TEAM"])
        else:
            winners.append(None)

    if (page == "index.html"):
        # An extra second of computation that is unnecessary for now. Commenting.
        # latest_power_ranking = get_reddit_power_ranking()
        latest_power_ranking = (False, False)
        hot_nba_posts = get_hot_nba_post()
        bball_breakdown_posts = get_bball_breakdown_articles()
        fansided_posts = get_fansided_articles()
        # hot_nba_post = (False, False)
        youtube_url = youtube_search("freedawkins", 2, True)

        pts_leaders_tiles = league.LeadersTiles()
        # Other stats that are commented because the extra computation time is not worth it.
        # rebs_leaders_tiles = league.LeadersTiles(stat_category="REB")
        # asts_leaders_tiles = league.LeadersTiles(stat_category="AST")

        # season_high_pts = pts_leaders_tiles.current_season_high()
        # season_high_rebs = rebs_leaders_tiles.current_season_high()
        # season_high_asts = asts_leaders_tiles.current_season_high()
        season_high_pts = False
        season_high_rebs = False
        season_high_asts = False
    else:
        latest_power_ranking = (False, False)
        hot_nba_posts = None
        bball_breakdown_posts = None
        fansided_posts = None
        youtube_url = False
        season_high_pts = False
        season_high_rebs = False
        season_high_asts = False

    return render_template(page, 
                           title=title,
                           date=datestring,
                           yesterday=datestring_yesterday,
                           tomorrow=datestring_tomorrow,
                           pretty_today=pretty_today,
                           pretty_yesterday=pretty_yesterday,
                           pretty_tomorrow=pretty_tomorrow,
                           games=enumerate(games),
                           winners=winners,
                           power_ranking_url=latest_power_ranking[0],
                           power_ranking_title=latest_power_ranking[1],
                           east_standings=enumerate(east_standings, 1),
                           west_standings=west_standings,
                           team=CITY_TO_TEAM,
                           hot_nba_posts=hot_nba_posts,
                           bball_breakdown_posts=bball_breakdown_posts,
                           fansided_posts=fansided_posts,
                           youtube_url=youtube_url,
                           season_high_pts=season_high_pts,
                           season_high_rebs=season_high_rebs,
                           season_high_asts=season_high_asts)

def get_reddit_power_ranking():
    """Gets latest /r/NBA Power Ranking from reddit.
    """
    subreddit = reddit.subreddit("nba")
    for submission in subreddit.search("Official /r/NBA Power Rankings", sort="new", limit=1):
        if (submission):
            return (submission.url, submission.title)
        else:
            return ("http://www.redditstatus.com/", "Reddit Status?")

def get_hot_nba_post():
    """Gets hottest /r/NBA post from reddit.
    """
    subreddit = reddit.subreddit("nba")
    submissions = []
    for submission in subreddit.top("day", limit=11):
        submissions.append(submission)
        
    return submissions
    """
        if (submission):
            return (submission.permalink, submission.title)
        else:
            return ("http://www.redditstatus.com/", "Reddit Status?")
    """

def get_games(date):
    """Get list of games in daily scoreboard.
    """
    scoreboard = nba_py.Scoreboard(month=date.month,
                                   day=date.day,
                                   year=date.year)
    line_score = scoreboard.line_score()
    game_header = scoreboard.game_header()

    games = []
    current_game = {}
    game_sequence = 0
    game_sequence_counter = 0

    # Get HOME TEAM and AWAY TEAM data for each boxscore game in line_score.
    for i, value in enumerate(line_score):
        if (value["GAME_SEQUENCE"] != game_sequence):
            game_sequence += 1

            current_game["GAME_ID"] = value["GAME_ID"]
            home_team_id = game_header[game_sequence - 1]["HOME_TEAM_ID"]

            if (home_team_id == value["TEAM_ID"]):
              current_game["HOME_TEAM"] = value["TEAM_ABBREVIATION"]
              current_game["HOME_TEAM_WINS_LOSSES"] = value["TEAM_WINS_LOSSES"]
              current_game["HOME_TEAM_PTS"] = value["PTS"]
              current_game["HOME_TEAM_ID"] = value["TEAM_ID"]
              if (current_game["HOME_TEAM"] in TEAM_ID_DATA):
                current_game["HOME_TEAM_IMG"] = TEAM_ID_DATA[current_game["HOME_TEAM"]]["img"]
            else:
              current_game["AWAY_TEAM"] = value["TEAM_ABBREVIATION"]
              current_game["AWAY_TEAM_WINS_LOSSES"] = value["TEAM_WINS_LOSSES"]
              current_game["AWAY_TEAM_PTS"] = value["PTS"]
              current_game["AWAY_TEAM_ID"] = value["TEAM_ID"]
              if (current_game["AWAY_TEAM"] in TEAM_ID_DATA):
                current_game["AWAY_TEAM_IMG"] = TEAM_ID_DATA[current_game["AWAY_TEAM"]]["img"]

            if (value["TEAM_ABBREVIATION"] in TEAMS):
                if (home_team_id == value["TEAM_ID"]):
                    current_game["HOME_TEAM_FULL_NAME"] = TEAMS[value["TEAM_ABBREVIATION"]]["city"] + \
                                                          " " + TEAMS[value["TEAM_ABBREVIATION"]]["name"]
                else:
                    current_game["AWAY_TEAM_FULL_NAME"] = TEAMS[value["TEAM_ABBREVIATION"]]["city"] + \
                                                          " " + TEAMS[value["TEAM_ABBREVIATION"]]["name"]
            
            game_sequence = value["GAME_SEQUENCE"]
            game_sequence_counter += 1
        elif game_sequence_counter == 1:
            if ("AWAY_TEAM" in current_game):
              current_game["HOME_TEAM"] = value["TEAM_ABBREVIATION"]
              current_game["HOME_TEAM_WINS_LOSSES"] = value["TEAM_WINS_LOSSES"]
              current_game["HOME_TEAM_PTS"] = value["PTS"]
              current_game["HOME_TEAM_ID"] = value["TEAM_ID"]
              if (current_game["HOME_TEAM"] in TEAM_ID_DATA):
                current_game["HOME_TEAM_IMG"] = TEAM_ID_DATA[current_game["HOME_TEAM"]]["img"]
            else:
              current_game["AWAY_TEAM"] = value["TEAM_ABBREVIATION"]
              current_game["AWAY_TEAM_WINS_LOSSES"] = value["TEAM_WINS_LOSSES"]
              current_game["AWAY_TEAM_PTS"] = value["PTS"]
              current_game["AWAY_TEAM_ID"] = value["TEAM_ID"]
              if (current_game["AWAY_TEAM"] in TEAM_ID_DATA):
                current_game["AWAY_TEAM_IMG"] = TEAM_ID_DATA[current_game["AWAY_TEAM"]]["img"]

            if (value["TEAM_ABBREVIATION"] in TEAMS):
                if ("AWAY_TEAM" in current_game):
                  current_game["HOME_TEAM_FULL_NAME"] = TEAMS[value["TEAM_ABBREVIATION"]]["city"] + \
                                                        " " + TEAMS[value["TEAM_ABBREVIATION"]]["name"]
                else:
                  current_game["AWAY_TEAM_FULL_NAME"] = TEAMS[value["TEAM_ABBREVIATION"]]["city"] + \
                                                        " " + TEAMS[value["TEAM_ABBREVIATION"]]["name"]

            current_game["GAME_STATUS_TEXT"] = game_header[game_sequence - 1]["GAME_STATUS_TEXT"]
            if not game_header[game_sequence - 1]["NATL_TV_BROADCASTER_ABBREVIATION"]:
                current_game["BROADCASTER"] = ""
            else:
                current_game["BROADCASTER"] = game_header[game_sequence - 1]["NATL_TV_BROADCASTER_ABBREVIATION"]

            games.append(current_game)

            current_game = {}

            game_sequence = value["GAME_SEQUENCE"]
            game_sequence_counter -= 1

    east_standings = scoreboard.east_conf_standings_by_day()
    west_standings = scoreboard.west_conf_standings_by_day()

    return (games, east_standings, west_standings)

@app.route('/boxscores/<gameid>')
def boxscores(gameid, season=CURRENT_SEASON):
    boxscore = game.Boxscore(gameid)

    player_stats = boxscore.player_stats()
    team_stats = boxscore.team_stats()

    len_player_stats = len(player_stats)
    len_team_stats = len(team_stats)
    num_starters = 5
    starters_title = True

    # Used to calculate the current season
    try:
      boxscore_summary = game.BoxscoreSummary(gameid)
    except:
      return render_template("boxscores.html",
                             title="boxscore",
                             len_team_stats=0)

    boxscore_game_summary = boxscore_summary.game_summary()
    home_team = boxscore_game_summary[0]["GAMECODE"][9:12]
    away_team = boxscore_game_summary[0]["GAMECODE"][12:16]

    if home_team in TEAM_ID_DATA:
      home_team_city = TEAM_ID_DATA[home_team]["city"]
      home_team_name = TEAM_ID_DATA[home_team]["name"]
      home_team_logo = TEAM_ID_DATA[home_team]["img"]
    else:
      home_team_logo = False

    if away_team in TEAM_ID_DATA:
      away_team_city = TEAM_ID_DATA[away_team]["city"]
      away_team_logo = TEAM_ID_DATA[away_team]["img"]
      away_team_name = TEAM_ID_DATA[away_team]["name"]
    else:
      away_team_logo = False

    boxscore_game_date = boxscore_game_summary[0]["GAME_DATE_EST"]
    datetime_boxscore = datetime.datetime.strptime(boxscore_game_date[:10], "%Y-%m-%d")
    pretty_date = datetime_boxscore.strftime("%b %d, %Y")

    # Get current season like "2016-17".
    to_year = int(boxscore_game_summary[0]["SEASON"])
    next_year = to_year + 1

    season = str(to_year) + "-" + str(next_year)[2:4]

    # Create NBA recap link.
    recap_date = datetime_boxscore.strftime("%Y/%m/%d")

    # Get nba recap video links for previous years like 2016 or before.
    # It takes 2 extra seconds. Commenting for now.
    # nba_recap = False
    """
    if (to_year < 2016):
        nba_recap = "http://www.nba.com/video/games/" + TEAM_ID_DATA[away_team]["name"] + "/" + recap_date + "/" + gameid + "-" + home_team + "-" + away_team + "-recap.nba"
        if not test_link(nba_recap):
            nba_recap = "http://www.nba.com/video/channels/playoffs/" + recap_date + "/" + gameid + "-" + home_team + "-" + away_team + "-recap.nba"

            if not test_link(nba_recap):
              nba_recap = False
    """
    if (to_year >= 2016):
        nba_recap = "http://www.nba.com/video/" + recap_date + "/" + gameid + "-" + home_team + "-" + away_team + "-recap"
        if not test_link(nba_recap):
            yesterday = datetime_boxscore - datetime.timedelta(1)
            recap_date = yesterday.strftime("%Y/%m/%d")
            nba_recap = "http://www.nba.com/video/" + recap_date + "/" + gameid + "-" + home_team + "-" + away_team + "-recap"
            if not test_link(nba_recap):
              nba_recap = False
    else:
        nba_recap = False

    # Figure out which team won or is winning.
    leading_points = 0
    winning = ""
    for i in team_stats:
        if i["PTS"] > leading_points:
            leading_points = i["PTS"]
            winning = i["TEAM_ABBREVIATION"]
        elif i["PTS"] < leading_points:
            continue
        else:
            winning = False

    # Add a 0 to a single digit minute like 4:20 to 04:20
    # Because bootstrap-datatable requires consistency.
    for i in player_stats:
        if (i["MIN"] and not isinstance(i["MIN"], int)):
            if (len(i["MIN"]) == 4):
                i["MIN"] = "0" + i["MIN"]

    if (len_team_stats != 0):
        team_summary_info = [team.TeamSummary(team_stats[0]["TEAM_ID"],
                                              season=season).info(),
                            team.TeamSummary(team_stats[1]["TEAM_ID"],
                                             season=season).info()]
    else:
        team_summary_info = False

    # Search for relevant reddit Post Game Thread.
    boxscore_line_score = boxscore_summary.line_score()

    """
    startTime = time.time()
    elapsedTime = time.time() - startTime
    elapsedTime = elapsedTime * 1000
    print(elapsedTime)
    """
    # post_game_thread = False
    post_game_thread = get_post_game_thread(next_year, boxscore_game_summary[0]["GAME_STATUS_TEXT"], boxscore_line_score, team_stats)

    # Get link for fullmatchtv (full broadcast video link). It takes 2 extra seconds. Commenting for now.
    full_match_url = False
    """
    if (next_year > 2016 and boxscore_game_summary[0]["GAME_STATUS_TEXT"] == "Final"):
        match_date = datetime_boxscore.strftime("%b-%-d-%Y")
        full_match_url = search_nba_full_match(away_team_city,
                                               away_team_name,
                                               home_team_city,
                                               home_team_name,
                                               match_date)
    else:
        full_match_url = False
    """

    if (team_stats and boxscore_game_summary[0]["GAME_STATUS_TEXT"] == "Final"):
        youtube_search_query = team_stats[0]["TEAM_CITY"] + " " + \
                               team_stats[0]["TEAM_NAME"] + " vs " + \
                               team_stats[1]["TEAM_CITY"] + " " + \
                               team_stats[1]["TEAM_NAME"] + " " + \
                               pretty_date
        youtube_url = youtube_search(youtube_search_query, 1)
    else:
        youtube_url = False

    inactive_players = boxscore_summary.inactive_players()
    officials = boxscore_summary.officials()

    return render_template("boxscores.html",
                           title="boxscore",
                           player_stats=player_stats,
                           len_player_stats=len_player_stats,
                           len_team_stats=len_team_stats,
                           starters_title=starters_title,
                           num_starters=num_starters,
                           team_stats=team_stats,
                           winning=winning,
                           team_summary_info=team_summary_info,
                           pretty_date=pretty_date,
                           boxscore_line_score=boxscore_line_score,
                           post_game_thread=post_game_thread,
                           home_team=home_team,
                           away_team=away_team,
                           home_team_logo=home_team_logo,
                           away_team_logo=away_team_logo,
                           nba_recap=nba_recap,
                           full_match_url=full_match_url,
                           youtube_url=youtube_url,
                           inactive_players=inactive_players,
                           officials=officials)

def test_link(link):
    """Test if link is valid.
    """
    r = requests.get(link)
    if (r.status_code != 200):
        return False
    else:
        return True

def get_post_game_thread(next_year, game_status_text, boxscore_line_score, team_stats):
    # Post Game Threads started appearing during the 2014-2015 season.
    if (next_year > 2014 and game_status_text == "Final"):
        subreddit = reddit.subreddit("nba")
        search_query = "[Post Game Thread] " + team_stats[0]["TEAM_CITY"] + " " + team_stats[0]["TEAM_NAME"] + \
                       " (" + boxscore_line_score[0]["TEAM_WINS_LOSSES"] + ") " + \
                       team_stats[1]["TEAM_CITY"] + " " + team_stats[1]["TEAM_NAME"] + \
                       " (" + boxscore_line_score[1]["TEAM_WINS_LOSSES"] + ")"
        for submission in subreddit.search(search_query, limit=1):
            if (submission):
                return (submission.url, submission.title)
            else:
                return ("http://www.redditstatus.com/", "Reddit Status?")
    else:
        return False

def search_nba_full_match(away_team_city,
                          away_team_name,
                          home_team_city,
                          home_team_name,
                          match_date):
    """Searches for nba full game recording from fullmatchtv.com
    """
    link_version_one = "http://fullmatchtv.com/"
    link_version_two = "http://fullmatchtv.com/"

    split_away_team_city = away_team_city.split()
    split_home_team_city = home_team_city.split()

    for i in split_away_team_city:
        link_version_one += i + "-"
    link_version_one += away_team_name + "-"

    for i in split_home_team_city:
        link_version_one += i + "-"
        link_version_two += i + "-"
    link_version_one += home_team_name + "-"
    link_version_two += home_team_name + "-"

    for i in split_away_team_city:
        link_version_two += i + "-"
    link_version_two += away_team_name + "-"

    link_version_one += match_date
    link_version_two += match_date

    if (test_link(link_version_one)):
        return link_version_one 
    elif (test_link(link_version_two)):
        return link_version_two
    else:
        return False

def youtube_search(q, max_results=25, freedawkins=None):
    """Searches YouTube for q and returns YouTube link.
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

    return False

@app.route('/players/<playerid>')
def players(playerid):
    """Specific player pages.
    """
    player_summary = player.PlayerSummary(playerid)
    player_summary_info = player_summary.info()
    headline_stats = player_summary.headline_stats()

    to_year = int(player_summary_info[0]["TO_YEAR"])
    next_year = to_year + 1

    season = str(to_year) + "-" + str(next_year)[2:4]

    birth_datestring = player_summary_info[0]["BIRTHDATE"][:10]
    birth_date = datetime.datetime.strptime(birth_datestring, "%Y-%m-%d")
    pretty_birth_date = birth_date.strftime("%m-%d-%Y")
    age = calculate_age(birth_date)

    player_game_logs = player.PlayerGameLogs(playerid, season=season)
    player_games = player_game_logs.info()

    playoffs_playergamelogs = player.PlayerGameLogs(playerid, season=season, season_type="Playoffs")
    playoffs_player_games = playoffs_playergamelogs.info()

    player_career = player.PlayerCareer(playerid)
    player_career_regular_season_totals = player_career.regular_season_totals()
    player_career_post_season_totals = player_career.post_season_totals()

    player_headshot = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/" + playerid + ".png"
    if (not test_link(player_headshot)):
        player_headshot = False

    return render_template("players.html",
                           title=player_summary_info[0]["DISPLAY_FIRST_LAST"],
                           playerid=playerid,
                           player_games=player_games,
                           playoffs_player_games=playoffs_player_games,
                           player_summary_info=player_summary_info[0],
                           headline_stats=headline_stats[0],
                           age=age,
                           pretty_birth_date=pretty_birth_date,
                           season=season,
                           player_career_regular_season_totals=player_career_regular_season_totals,
                           player_career_post_season_totals=player_career_post_season_totals,
                           team_img=TEAM_ID_DATA,
                           player_headshot=player_headshot)

def calculate_age(born):
    """Calculates the person's age by subtracting DOB by today's date.
    """
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

@app.route('/players/<playerid>/season/<season>/')
def players_and_season(playerid, season):
    # season example: "2016-17"
    # type example: "Regular Season" or "Playoffs" 
    player_game_logs = player.PlayerGameLogs(playerid,
                                             season=season)
    player_games = player_game_logs.info()

    playoffs_playergamelogs = player.PlayerGameLogs(playerid,
                                                    season=season,
                                                    season_type="Playoffs")
    playoffs_player_games = playoffs_playergamelogs.info()

    player_summary = player.PlayerSummary(playerid)
    player_summary_info = player_summary.info()
    headline_stats = player_summary.headline_stats()

    birth_datestring = player_summary_info[0]["BIRTHDATE"][:10]
    birth_date = datetime.datetime.strptime(birth_datestring, "%Y-%m-%d")
    pretty_birth_date = birth_date.strftime("%m-%d-%Y")
    age = calculate_age(birth_date)

    player_headshot = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/" + playerid + ".png"
    if (not test_link(player_headshot)):
        player_headshot = False

    return render_template("players.html",
                           title=player_summary_info[0]["DISPLAY_FIRST_LAST"],
                           player_games=player_games,
                           playoffs_player_games=playoffs_player_games,
                           player_summary_info=player_summary_info[0],
                           headline_stats=headline_stats[0],
                           age=age,
                           pretty_birth_date=pretty_birth_date,
                           season=season,
                           team_img=TEAM_ID_DATA,
                           player_headshot=player_headshot)

@app.route('/teams/<teamid>')
def teams(teamid):
    """Specific team pages.
    """
    team_summary = team.TeamSummary(teamid)
    team_summary_info = team_summary.info()
    team_season_ranks = team_summary.season_ranks()

    team_common_roster = team.TeamCommonRoster(teamid)
    roster = team_common_roster.roster()
    coaches = team_common_roster.coaches()

    season = team_summary_info[0]["SEASON_YEAR"]

    team_game_log = team.TeamGameLogs(teamid,
                                      season=season)
    team_games = team_game_log.info()

    playoffs_teamgamelogs = team.TeamGameLogs(teamid,
                                              season=season,
                                              season_type="Playoffs")
    playoffs_team_games = playoffs_teamgamelogs.info()

    team_season = team.TeamSeasons(teamid)
    team_season_info = team_season.info()

    for i in team_season_info:
        if (i["YEAR"] == season):
            current_season_info = i

    return render_template("teams.html",
                           title=team_summary_info[0]["TEAM_CITY"] + " " + team_summary_info[0]["TEAM_NAME"],
                           teamid=teamid,
                           team_summary_info=team_summary_info,
                           team_season_ranks=team_season_ranks,
                           season=season,
                           team_games=team_games,
                           playoffs_team_games=playoffs_team_games,
                           team_season=team_season_info,
                           roster=roster,
                           coaches=coaches,
                           current_season_info=current_season_info,
                           team_img=TEAM_ID_DATA)

@app.route('/teams/<teamid>/season/<season>/')
def teams_and_season(teamid, season):
    # season example: "2016-17"
    # type example: "Regular Season" or "Playoffs" 
    team_game_log = team.TeamGameLogs(teamid,
                                      season=season)
    team_games = team_game_log.info()

    playoffs_teamgamelogs = team.TeamGameLogs(teamid,
                                              season=season,
                                              season_type="Playoffs")
    playoffs_team_games = playoffs_teamgamelogs.info()

    team_summary = team.TeamSummary(teamid,
                                    season=season)
    team_summary_info = team_summary.info()
    team_season_ranks = team_summary.season_ranks()

    team_common_roster = team.TeamCommonRoster(teamid)
    roster = team_common_roster.roster()
    coaches = team_common_roster.coaches()

    team_season = team.TeamSeasons(teamid)
    team_season_info = team_season.info()

    for i in team_season_info:
        if (i["YEAR"] == season):
            current_season_info = i

    return render_template("teams.html",
                           title=team_summary_info[0]["TEAM_CITY"] + " " + team_summary_info[0]["TEAM_NAME"],
                           teamid=teamid,
                           team_summary_info=team_summary_info,
                           team_season_ranks=team_season_ranks,
                           season=season,
                           team_games=team_games,
                           playoffs_team_games=playoffs_team_games,
                           current_season_info=current_season_info,
                           team_img=TEAM_ID_DATA)

@app.route('/playervsplayer')
def player_vs_player():
    leaders = league.Leaders(stat_category="EFF")

    player_leaders = leaders.results()

    return render_template("playervsplayer.html",
                           title="Player vs Player",
                           player_leaders=player_leaders,
                           teams=TEAMS)

@app.route('/teamvsteam')
def team_vs_team():
    """Comparing team lineups.
    """
    league_dash_lineups = league.Lineups()
    league_dash_lineups_overall = league_dash_lineups.overall()

    for i in league_dash_lineups_overall:
      new_group_name = ""
      split_group_name = i["GROUP_NAME"].split("-")
      for j, value in enumerate(split_group_name):
        first_last = ' '.join(reversed(value.split(',')))
        if (j != len(split_group_name) - 1):
          new_group_name += first_last + " - "
        else:
          new_group_name += first_last
      i["GROUP_NAME"] = new_group_name

    return render_template("teamvsteam.html",
                           title="Team vs Team",
                           league_dash_lineups=league_dash_lineups_overall)

@app.route('/draftcombine/<season>', methods=['GET', 'POST'])
def draft_combine(season):
    """Draft combine page.
    """
    if request.method == "GET":
      year = int(season)
    else:
      year = int(request.form["season"])

    next_year = year + 1
    next_year_string = str(next_year)[2:4]
    season_name = str(year) + "-" + next_year_string

    draft_combine_summary = draftcombine.Summary(season=season_name)
    draft_combine_summary_overall = draft_combine_summary.overall()

    if (int(year) > 1999):
      year = int(draft_combine_summary_overall[0]["SEASON"])
    else:
      year = False

    return render_template("draftcombine.html",
                           title="Draft Combine " + str(year),
                           draft_combine_summary=draft_combine_summary_overall,
                           year=year)

@app.route('/search', methods=["POST"])
def search():
    """Search post request when searching for a specific player or team.
    """
    name = request.form["searchname"]
    if name.upper() == "YAO MING":
        return redirect(url_for("players", playerid="2397"))

    team_id = ""
    split_name = name.split(" ", 1)
    if (len(split_name) == 1):
        try:
            get_player = player.get_player(split_name[0], just_id=False)
            get_team = False
        except:
            get_player = False
            if (split_name[0].upper() in TEAMS):
                team_id = TEAMS[split_name[0].upper()]["id"]
                team_summary = team.TeamSummary(team_id)
                get_team = team_summary.info()
            else:
                get_team = False
    else:
        try:
            get_player = player.get_player(split_name[0], last_name=split_name[1], just_id=False)
            get_team = False
        except:
            get_player = False
            if (name.lower() in TEAM_NAME_TO_ID):
                team_id = TEAM_NAME_TO_ID[name.lower()]["id"]
                team_summary = team.TeamSummary(team_id)
                get_team = team_summary.info()
            else:
                get_team = False

    if get_player:
        return redirect(url_for("players", playerid=get_player["PERSON_ID"]))
    elif get_team:
        return redirect(url_for("teams", teamid=team_id))
    else:
        return render_template("search.html")

def remove_unicode_in_dict(data):
    """Removes unicode strings from dictionaries.

    Args:
        data: dict that you want to remove unicode strings from.
    """
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(remove_unicode_in_dict, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(remove_unicode_in_dict, data))
    else:
        return data

def get_live_game_data():
    """Get full live game data. Incomplete function.
    """
    nbc_scores_link = "http://msnbchosted.stats.com/nba/scoreboard.asp?day="

    r = requests.get(nbc_scores_link)
    print(r.text)

    # soup = BeautifulSoup(html_doc, 'html.parser')

    pass

def get_bball_breakdown_articles():
    """Get a dictionary of the latest bballbreakdown articles.
    """
    bball_breakdown_link = "http://bballbreakdown.com/category/articles/"

    r = requests.get(bball_breakdown_link)
    bball_breakdown_html = r.text

    soup = BeautifulSoup(bball_breakdown_html, "html.parser")
    # print(soup.prettify())

    cat_slider_items = soup.find_all("div",
                                     {"class": "cat-slider-item"})

    bball_breakdown_dict = {}

    for div in cat_slider_items:
      bball_breakdown_dict[div.find('h2').string] = div.find('a')['href']

    return bball_breakdown_dict

def get_fansided_articles():
    """Get a dictionary of the latest fansided articles.
    """
    fansided_link = "http://fansided.com/nba/the-step-back/nylon-calculus/"

    r = requests.get(fansided_link)
    fansided_html = r.text

    soup = BeautifulSoup(fansided_html, "html.parser")
    # print(soup.prettify())

    fansided_articles = soup.find_all("h2",
                                      {"class": "title"})

    fansided_dict = {}

    for div in fansided_articles:
        fansided_dict[div.find('a')['title']] = div.find('a')['href']

    return fansided_dict
      
if __name__ == "__main__":
    # Run officially on a web server.
    # app.run(threaded=True)
    # Run on localhost with port 8080.
    app.run(host='0.0.0.0', port=8080, threaded=True)
