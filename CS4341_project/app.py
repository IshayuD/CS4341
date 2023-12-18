import webbrowser
import os
from flask import Flask, render_template, jsonify, request, send_file
import webbrowser
import json
import databridge
import datacleaner
import datagrabber
from teammanager import TeamManager
import ReturnJSONFromSQL
import ReturnAVGs

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
avg_list = ReturnAVGs.avg_list
avg_PTS = 10.68
avg_REB = 3.84
avg_AST = 2.36
avg_STL = 0.7
avg_BLK = 0.42

#Recommened Players
data_list = ReturnJSONFromSQL.data_list
#data_json = json.dumps(data_list)
print(data_list)

@app.route("/")
def home():
    return render_template("index.html", 
                           avg_PTS = avg_PTS, 
                           avg_REB = avg_REB, 
                           avg_AST = avg_AST, 
                           avg_STL = avg_STL, 
                           avg_BLK = avg_BLK,
                           data_list = data_list)

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
