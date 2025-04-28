from flask import Flask, jsonify
from flask_cors import CORS
from nba_api.stats.endpoints import playercareerstats, playergamelog
from nba_api.stats.static import players



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
    game_stats = playergamelog.PlayerGameLog(player_id=player_id, season='2024-25')
    stats_df = game_stats.get_data_frames()[0]

    return jsonify(stats_df.to_dict(orient='records')[0])
# route to lebron's stats from a random notable game
@app.route('/api/lebron/random-game', methods=['GET'])
def get_lebron_random_game_stats():
    career_game_stats = playergamelog.PlayerGameLog(player_id=player_id)
    stats_df = career_game_stats.get_data_frames()[0]
    notable_games = stats_df[stats_df['PTS'] + stats_df['REB'] + stats_df['AST'] >= 50]
    random_game = notable_games.sample(n=1).iloc[0]
    return jsonify(random_game.to_dict())

if __name__ == '__main__':
    app.run(debug=True)