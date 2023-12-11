import datacleaner as dc
import datagrabber as dg


def test_get_overall_averages():
    player_data = dg.get_player_data(path='../data/NBA_Player_Stats.csv')
    cleaned_data = dc.clean_data(player_data)

    print(cleaned_data)
    print(type(cleaned_data))