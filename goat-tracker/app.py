from flask import Flask, jsonify, request
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
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [item['contentDetails']['videoId'] for item in data.get('items', [])]
    except requests.RequestException as e:
        print("YouTube API error:", e)
        return []

def pick_daily_video(video_ids):
    if not video_ids:
        return None
    today = datetime.date.today()
    index = today.toordinal() % len(video_ids)
    return video_ids[index]

# ---- Load LeBron's data once on startup ----

lebron = [player for player in players.get_players() if player['full_name'] == 'LeBron James'][0]
player_id = lebron['id']

def fetch_notable_games(season_type):
    all_games = pd.DataFrame()
    for year in range(2003, 2024):
        season = f"{year}-{str(year+1)[-2:]}"
        try:
            season_stats = playergamelog.PlayerGameLog(
                player_id=player_id,
                season=season,
                season_type_all_star=season_type
            )
            stats_df = season_stats.get_data_frames()[0]
            all_games = pd.concat([all_games, stats_df], ignore_index=True)
            time.sleep(0.5)
        except Exception as e:
            print(f"Error fetching {season_type} for {season}:", e)
    return all_games[all_games['PTS'] + all_games['REB'] + all_games['AST'] >= 50]

notable_regular_season_games = fetch_notable_games("Regular Season")
notable_playoff_games = fetch_notable_games("Playoffs")

# ---- API Routes ----

@app.route('/api/lebron/career-stats', methods=['GET'])
def get_lebron_career_stats():
    try:
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        stats_df = career_stats.get_data_frames()[0]
        return jsonify(stats_df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/lebron/recent-game', methods=['GET'])
def get_lebron_game_stats():
    season_type = request.args.get('season_type', default='Regular Season')
    try:
        game_stats = playergamelog.PlayerGameLog(
            player_id=player_id,
            season='2024-25',
            season_type_all_star=season_type
        )
        stats_df = game_stats.get_data_frames()[0]
        return jsonify(stats_df.to_dict(orient='records')[0])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/lebron/random-game', methods=['GET'])
def get_lebron_random_game_stats():
    season_type = request.args.get('season_type', default='Regular Season')
    if season_type == 'Regular Season':
        notable_games = notable_regular_season_games
    elif season_type == 'Playoffs':
        notable_games = notable_playoff_games
    else:
        return jsonify({"error": "Invalid season type. Please use 'Regular Season' or 'Playoffs'."}), 400
    if notable_games.empty:
        return jsonify({"error": "No data available."}), 503
    random_game = notable_games.sample(n=1).iloc[0]
    return jsonify(random_game.to_dict())

@app.route('/api/lebron/random-video', methods=['GET'])
def get_random_video():
    video_ids = get_video_ids()
    random_video_id = pick_daily_video(video_ids)
    if not random_video_id:
        return "<h1>No highlight videos are available right now. Please try again later.</h1>", 503
    return jsonify({"video_id": random_video_id})

port = int(os.getenv('PORT', 5000))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
