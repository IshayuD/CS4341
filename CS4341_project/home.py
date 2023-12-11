import databridge
import datacleaner
import datagrabber
from teammanager import TeamManager


def main():
    # UI
    file_path = 'CS4341_project/pages/home.html'
    # webbrowser.open_new_tab('file://' + os.path.realpath(file_path))  # Opens HTML file in new tab
    # TODO Make webpage open
    # Python
    initialize_players_and_teams()


def initialize_players_and_teams() -> None:
    """
    Initializes the players and teams.
    """
    # TODO: Fix data_path
    # data_path = 'CS4341_project/data/NBA_Player_Stats.csv'
    tm = TeamManager()
    data_path = 'data/NBA_Player_Stats.csv'
    player_data = datagrabber.get_player_data(path=data_path)
    cleaned_data = datacleaner.clean_data(player_data)
    players = databridge.create_players_from_data(cleaned_data, tm)


if __name__ == '__main__':
    main()
