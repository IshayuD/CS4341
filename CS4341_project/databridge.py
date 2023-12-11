import numpy

import teammanager
from player import Player
from team import Team, TooManyPlayersError


# This class is the bridge between the data and the python code.

def create_players_from_data(data: list[numpy.record], team_manager: teammanager.TeamManager) -> list[Player]:
    """
    Creates instances of Player from the data. Use datacleaner.clean_data() before creating players.
    :param data: The data from datacleaner.clean_data() to create players from.
    :param team_manager: The TeamManager to update with the new players
    :return: A list of Player instances.
    """
    players = []
    for player in data:
        # All data from file
        name = player[1]
        position = player[2]
        age = player[3]
        games = player[9]
        games_started = player[10]
        minutes_played = player[11]
        current_team = player[8]
        point_avg = player[4]
        assist_avg = player[5]
        steal_avg = player[6]
        block_avg = player[7]

        # Instantiate new player
        new_player = Player(name, position, age, games, games_started, minutes_played, current_team, point_avg,
                            assist_avg, steal_avg, block_avg)

        # Add player to list of players
        players.append(new_player)
        team_manager.update_teams(new_player=new_player, current_team=current_team)
    return players
