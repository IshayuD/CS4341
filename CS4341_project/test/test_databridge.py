import datacleaner as dc
import datagrabber as dg
import databridge as db


def test_create_players_from_data():
    player_data = dg.get_player_data(path='../data/NBA_Player_Stats.csv')
    cleaned_data = dc.clean_data(player_data)
    print(db.create_players_from_data(cleaned_data))
