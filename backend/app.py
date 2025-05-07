from flask import Flask, jsonify, request
from flask_cors import CORS
from nba_api.stats.endpoints import playercareerstats, playergamelog
from nba_api.stats.static import players
import pandas as pd
import time  # Added for delay between API requests

app = Flask(__name__)
CORS(app)

lebron = [player for player in players.get_players() if player['full_name'] == 'LeBron James'][0]
player_id = lebron['id']

# Getting the stats for every game LeBron has played in the NBA, so that I can filter for notable games later

# regular season stats
regular_season_df = pd.DataFrame()
season_type = 'Regular Season'

for year in range(2003, 2024):
    season = f"{year}-{str(year+1)[-2:]}"
    season_stats = playergamelog.PlayerGameLog(player_id=player_id, season=season, season_type_all_star=season_type)
    stats_df = season_stats.get_data_frames()[0]
    regular_season_df = pd.concat([regular_season_df, stats_df], ignore_index=True)
    time.sleep(0.5)  # Add delay to avoid timeouts or rate limits

# Notable games are defined as games where the sum of points, rebounds, and assists is greater than or equal to 50

notable_regular_season_games = regular_season_df[regular_season_df['PTS'] + regular_season_df['REB'] + regular_season_df['AST'] >= 50]

# playoffs stats
playoffs_df = pd.DataFrame()
season_type = 'Playoffs'

for year in range(2003, 2024):
    season = f"{year}-{str(year+1)[-2:]}"
    season_stats = playergamelog.PlayerGameLog(player_id=player_id, season=season, season_type_all_star=season_type)
    stats_df = season_stats.get_data_frames()[0]
    playoffs_df = pd.concat([playoffs_df, stats_df], ignore_index=True)
    time.sleep(0.5)  # Add delay here too

notable_playoff_games = playoffs_df[playoffs_df['PTS'] + playoffs_df['REB'] + playoffs_df['AST'] >= 50]

@app.route('/')
def home():
    return jsonify({"Info": "Hello! This is the backend to Daniel's Goat Tracker app, a dashboard that displays Lebron James' career stats."})

# route to lebron's career stats, split up by season
@app.route('/api/lebron/career-stats', methods=['GET'])
def get_lebron_career_stats():
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    stats_df = career_stats.get_data_frames()[0]
    return jsonify(stats_df.to_dict(orient='records'))

# route to lebron's stats his most recent game
@app.route('/api/lebron/recent-game', methods=['GET'])
def get_lebron_game_stats():
    season_type = request.args.get('season_type', default='Regular Season')
    game_stats = playergamelog.PlayerGameLog(player_id=player_id, season='2024-25', season_type_all_star=season_type)
    stats_df = game_stats.get_data_frames()[0]
    return jsonify(stats_df.to_dict(orient='records')[0])

# route to lebron's stats from a random notable game
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

if __name__ == '__main__':
    app.run(debug=True)
