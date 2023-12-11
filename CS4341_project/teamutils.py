positions = {'C': 'Center', 'PF': 'Power Forward', 'SF': 'Small Forward', 'PG': 'Point Guard', 'SG': 'Shooting Guard'}
acronyms = {'Rk': 'Rank', 'Player': 'Player', 'Pos': 'Position', 'Age': 'Age', 'PTS': 'Points', 'AST': 'Assists',
            'STL': 'Steals', 'BLK': 'Blocks', 'Tm': 'Team', 'G': 'Games', 'GS': 'Games Started', 'MP': 'Minutes Played'}
all_averages = ['point_avg', 'assist_avg', 'steal_avg', 'block_avg']


def is_valid_position(position: str) -> bool:
    """
    Checks if the provided position is a valid position
    :param position: The position to check
    :return: True if it is a valid position (in positions, or is two valid positions separated by a -), False otherwise
    """
    # Item in positions
    if positions.__contains__(position):
        return True

    # Not within positions
    positions_as_list = position.split('-')
    valid_position = True
    for sub_position in positions_as_list:
        if not positions.__contains__(sub_position):
            valid_position = False
    return valid_position
