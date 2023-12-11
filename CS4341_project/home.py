import webbrowser
import os

import databridge
import datacleaner
import datagrabber
from player import Player
from team import Team, TeamNotFoundError

teams = []


def main():
    # UI
    file_path = 'CS4341_project/pages/home.html'
    webbrowser.open_new_tab('file://' + os.path.realpath(file_path))  # Opens HTML file in new tab

    # Python
    initialize_players_and_teams()


def initialize_players_and_teams() -> None:
    """
    Initializes the players and teams.
    """
    data_path = 'CS4341_project/data/NBA_Player_Stats.csv'
    # data_path = 'data/NBA_Player_Stats.csv'
    player_data = datagrabber.get_player_data(path=data_path)
    cleaned_data = datacleaner.clean_data(player_data)
    players = databridge.create_players_from_data(cleaned_data)
    # TODO: BUG: Teams is always empty at the end for some reason
    print(*teams)

def add_team(team: Team) -> None:
    """
    Adds a team to the teams list
    :param team:
    :raises TeamExistsError: Raised if the team already exists
    """
    if is_existing_team(team):
        raise TeamExistsError(team=team)
    teams.append(team)


def is_existing_team(team: Team | str) -> bool:
    """
    Checks if the provided team is already in the teams list
    :param team: The team to check
    :return: True if the team is already in the teams list, False otherwise
    """
    if type(team) is str:
        for team_inst in teams:
            if team_inst.name == team:
                return True
        return False
    return any(team == t for t in teams)


def get_team(team_name: str) -> Team:
    """
    :param team_name: The name of the team to get
    :return: The team
    :raises TeamNotFoundError: Raised if the provided team is not found
    """
    for team_inst in teams:
        if team_inst.name == team_name:
            return team_inst
    raise TeamNotFoundError(team_name)

def print_teams():
    print(*teams)

class TeamExistsError(Exception):
    def __init__(self, message="The team already exists!", team=None):
        self.team = team
        self.message = message
        if team is not None:
            if type(team) is Team:
                self.message = "The team, " + team.name + ", is already a team!"
            elif type(team) is str:
                self.message = "The team, " + team + ", is already a team!"

        super().__init__(self.message)


if __name__ == '__main__':
    main()
