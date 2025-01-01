from flask import Flask, jsonify
from flask_cors import CORS
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

app = Flask(__name__)
CORS(app)  # Allows your React app to access the backend

# Example route
@app.route('/')
def home():
    return jsonify({"message": "Hello from Flask!"})

# route to lebron's stats
@app.route('/api/lebron-stats', methods=['GET'])
def get_lebron_stats():
    lebron = [player for player in players.get_players() if player['full_name'] == 'LeBron James'][0]
    player_id = lebron['id']

    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    stats_df = career_stats.get_data_frames()[0]

    return jsonify(stats_df.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)