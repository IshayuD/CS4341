import webbrowser
import os
from flask import Flask, render_template, jsonify, request, send_file
import webbrowser
import databridge
import datacleaner
import datagrabber
from teammanager import TeamManager

app = Flask(__name__)

def main():
    # UI
    file_path = 'CS4341_project/pages/home.html'
    webbrowser.open_new_tab('file://' + os.path.realpath(file_path))  # Opens HTML file in new tab

tm = TeamManager()
data_path = 'CS4341_project/data/NBA_Player_Stats.csv'
# data_path = 'data/NBA_Player_Stats.csv'
player_data = datagrabber.get_player_data(path=data_path)
cleaned_data = datacleaner.clean_data(player_data)
players = databridge.create_players_from_data(cleaned_data, tm)

# Stat average values
avg_PTS = 1
avg_REB = 2
avg_AST = 3
avg_STL = 4
avg_BLK = 5

# Recommended Players
recPlayer1 = ""
recPlayer2 = ""
recPlayer3 = ""
recPlayer4 = ""

@app.route("/")
def home():
    return render_template("index.html", 
                           avg_PTS = avg_PTS, 
                           avg_REB = avg_REB, 
                           avg_AST = avg_AST, 
                           avg_STL = avg_STL, 
                           avg_BLK = avg_BLK)

@app.route("/get_csv")
def get_csv():
    return send_file('data/NBA_Player_Stats.csv', as_attachment=True)

@app.route("/save_json", methods=['POST'])
def save_json():
    data = request.is_json
    print('Received JSON data:', data)
    return jsonify({'message': 'JSON data received successfully'})


if __name__ == '__main__':
    app.run(debug=True)
