import numpy

from teamutils import all_averages

player_names = []  # A set of all players that have been looked at


def clean_data(data: numpy.recarray) -> list[numpy.record]:
    """
    :param data: The data to remove duplicate players from
    :return: a recarray with no duplicate players
    """
    cleaned_data = []

    # Loop through data
    for player in data:
        player_data = get_all_player_data(data, player.__getitem__(1))

        # Ensure no duplicates
        # player_data is None if the player was already added to list of players
        if player_data is None:
            continue

        # If there is only one instance of the player, no need to compute new averages
        if len(player_data) == 1:
            player_names.append(player.__getitem__(1))
            cleaned_data.append(player_data.__getitem__(0))
            continue

        get_overall_averages(player_data)
        # Add player name to list of already done players
        player_names.append(player.__getitem__(1))

    return cleaned_data


def get_overall_averages(data: list[numpy.record]) -> None:
    """
    A player can be in the dataset multiple times if they were on multiple teams, so getting the overall averages of
    the player will better represent their scores
    :param data: The CLEANED data of all players
    """
    player = data.__getitem__(0)
    average_indexes = {'point_avg': 4, 'assist_avg': 5, 'steal_avg': 6, 'block_avg': 7}

    for data_index in range(len(data)):
        if data_index == 0:
            continue
        for avg in all_averages:
            avg_index = average_indexes[avg]
            player.__setitem__(avg_index, add_average_from_average(data.__getitem__(data_index).__getitem__(avg_index),
                                                                   player.__getitem__(avg_index), data_index))
            continue


def get_all_player_data(data: numpy.recarray, player_name: str) -> list[numpy.record] | None:
    """
    Get all the player data of player_name
    :param data: The data of all players
    :param player_name: The name of the player to get the data of
    :return: A list of all the player_name records, or None if the player is already in player_names
    """
    if player_names.__contains__(player_name):
        return None

    all_data = []
    for player in data:
        if player.__getitem__(1) == player_name:
            all_data.append(player)
    return all_data


def add_average_from_average(new: float, old: float, count: int) -> float:
    """
    (Old Average * Old Count) + Added Average / New Count = New Average
    :param new: The new average to add
    :param old: The old average to compute from
    :param count: The number of items in new
    :return: The new average
    """
    if count == 0:
        raise ArithmeticError("Count should be greater than 0!")

    # Prevent a divide by 0
    if count == 1:
        return new

    # (Old Average * Old Count) + Added Average / New Count = New Average
    return (old * (count - 1) + new) / count
