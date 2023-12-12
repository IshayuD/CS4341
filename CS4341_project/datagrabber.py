import os
import numpy
import pandas as pd


def get_player_data(path='data/NBA_Player_Stats.csv') -> numpy.recarray:
    """
    Read the provided CSV file for player data.\n
    Columns are: 'Player', 'Pos', 'Age', 'PTS', 'AST', 'STL', 'BLK', 'Tm', 'G', 'GS', 'MP'
    :param path: The path to the data CSV file. Default is 'data/NBA_Player_Stats.csv'
    :return: A numpy.recarray of records, representing the data
    """
    player_csv_data_path = os.path.realpath(path)
    data_columns = ['Player', 'Pos', 'Age', 'PTS', 'AST', 'STL', 'BLK', 'Tm', 'G', 'GS', 'MP']

    # Use usecols to ignore the Rank column
    file = pd.read_csv(player_csv_data_path, usecols=data_columns)
    return file.to_records()
