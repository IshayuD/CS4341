import datagrabber as dg


def test_get_player_data():
    player_data = dg.get_player_data(path='../data/NBA_Player_Stats.csv')
    assert player_data is not None, "Player data was not obtained properly"
    print(player_data)
    print(type(player_data))