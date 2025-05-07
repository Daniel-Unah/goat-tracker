from flask import Flask, jsonify, request
from flask_cors import CORS
from nba_api.stats.endpoints import playercareerstats, playergamelog
from nba_api.stats.static import players
import pandas as pd



app = Flask(__name__)
CORS(app)

lebron = [player for player in players.get_players() if player['full_name'] == 'LeBron James'][0]
player_id = lebron['id']

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
    # Notable games are defined as games where the sum of points, rebounds, and assists is greater than or equal to 50
    all_stats_df = pd.DataFrame()
    for year in range(2003, 2024):
        season = f"{year}-{str(year+1)[-2:]}"
        season_stats = playergamelog.PlayerGameLog(player_id=player_id, season=season, season_type_all_star=season_type)
        stats_df = season_stats.get_data_frames()[0]
        all_stats_df = pd.concat([all_stats_df, stats_df], ignore_index=True)
    notable_games = all_stats_df[all_stats_df['PTS'] + all_stats_df['REB'] + all_stats_df['AST'] >= 50]
    random_game = notable_games.sample(n=1).iloc[0]
    return jsonify(random_game.to_dict())

if __name__ == '__main__':
    app.run(debug=True)