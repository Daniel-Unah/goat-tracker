from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from nba_api.stats.endpoints import playercareerstats, playergamelog
from nba_api.stats.static import players
import pandas as pd
import time
from dotenv import load_dotenv
import os
import requests
import random
import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
PLAYLIST_ID = 'PLAGEP4tf7sFs2iHSyLDM1STJ0udqXT8f5'

def get_video_ids():
    url = 'https://www.googleapis.com/youtube/v3/playlistItems'
    params = {
        'part': 'contentDetails',
        'maxResults': 50,
        'playlistId': PLAYLIST_ID,
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params, timeout = 5)
    if response.status_code != 200:
        print("Failed to fetch playlist:", response.text)
        return []
    data = response.json()
    return [item['contentDetails']['videoId'] for item in data.get('items', [])]

def pick_daily_video(video_ids):
    if not video_ids:
        return None
    today = datetime.date.today()
    index = today.toordinal() % len(video_ids)
    return video_ids[index]

lebron = [player for player in players.get_players() if player['full_name'] == 'LeBron James'][0]
player_id = lebron['id']

# Regular season stats
regular_season_df = pd.DataFrame()
season_type = 'Regular Season'
for year in range(2003, 2024):
    season = f"{year}-{str(year+1)[-2:]}"
    season_stats = playergamelog.PlayerGameLog(player_id=player_id, season=season, season_type_all_star=season_type)
    stats_df = season_stats.get_data_frames()[0]
    regular_season_df = pd.concat([regular_season_df, stats_df], ignore_index=True)
    time.sleep(0.5)

notable_regular_season_games = regular_season_df[regular_season_df['PTS'] + regular_season_df['REB'] + regular_season_df['AST'] >= 50]

# Playoffs stats
playoffs_df = pd.DataFrame()
season_type = 'Playoffs'
for year in range(2003, 2024):
    season = f"{year}-{str(year+1)[-2:]}"
    season_stats = playergamelog.PlayerGameLog(player_id=player_id, season=season, season_type_all_star=season_type)
    stats_df = season_stats.get_data_frames()[0]
    playoffs_df = pd.concat([playoffs_df, stats_df], ignore_index=True)
    time.sleep(0.5)

notable_playoff_games = playoffs_df[playoffs_df['PTS'] + playoffs_df['REB'] + playoffs_df['AST'] >= 50]

@app.route('/')
def home():
    return jsonify({"Info": "Hello! This is the backend to Daniel's Goat Tracker app, a dashboard that displays LeBron James' career stats."})

@app.route('/api/lebron/career-stats', methods=['GET'])
def get_lebron_career_stats():
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    stats_df = career_stats.get_data_frames()[0]
    return jsonify(stats_df.to_dict(orient='records'))

@app.route('/api/lebron/recent-game', methods=['GET'])
def get_lebron_game_stats():
    season_type = request.args.get('season_type', default='Regular Season')
    game_stats = playergamelog.PlayerGameLog(player_id=player_id, season='2024-25', season_type_all_star=season_type)
    stats_df = game_stats.get_data_frames()[0]
    return jsonify(stats_df.to_dict(orient='records')[0])

@app.route('/api/lebron/random-game', methods=['GET'])
def get_lebron_random_game_stats():
    season_type = request.args.get('season_type', default='Regular Season')
    if season_type == 'Regular Season':
        notable_games = notable_regular_season_games
    elif season_type == 'Playoffs':
        notable_games = notable_playoff_games
    else:
        return jsonify({"error": "Invalid season type. Please use 'Regular Season' or 'Playoffs'."}), 400
    random_game = notable_games.sample(n=1).iloc[0]
    return jsonify(random_game.to_dict())

@app.route('/api/lebron/random-video', methods=['GET'])
def get_random_video():
    video_ids = get_video_ids()
    random_video_id = pick_daily_video(video_ids)

    if not random_video_id:
        return "<h1>No highlight videos are available right now. Please try again later.</h1>", 503

    return jsonify({
        "video_id": random_video_id,
    })

if __name__ == '__main__':
    app.run(debug=True)
