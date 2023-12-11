import numpy
from player import Player
from home import is_existing_team, add_team, get_team, print_teams
from team import Team


# This class is the bridge between the data and the python code.

def create_players_from_data(data: list[numpy.record]) -> list[Player]:
    """
    Creates instances of Player from the data. Use datacleaner.clean_data() before creating players.
    :param data: The data from datacleaner.clean_data() to create players from.
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

        if is_existing_team(current_team):
            # Add to existing team
            new_team = get_team(current_team)
            new_team.add_player(new_player)
            continue

        # Create team
        new_team = Team(name=current_team, player_count=0, cap_space=0, point_avg=0, assist_avg=0, steal_avg=0,
                        block_avg=0)
        new_team.add_player(new_player)

        # Add team
        add_team(new_team)
    return players
