"""
This file implements 3 functions, all testing various parts of the data
processing file

These functions all use 2 smaller test csvs I made to easily calculate the
correct answers. However, they should still work with the full dataset

test_medal_score takes in a path to tiny_olympic.csv
It tests whether the medal_score column is correctly added
to the dataframe, and if the math lines up with what we'd expect


test_game_type takes in a path to tiny_olympic.csv
It tests whether the games_type column is correctly added to the 
dataframe, and if the string extraction worked correctly to set it
to the correct type of Olympic games


test_worldcup_champion takes in a path to tiny_worldcup.csv
It tests whether the wc_score column is correctly added to the
dataframe, and if the champion is correctly detected.
"""

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'code'))
from data_processor import load_olympic_data, load_world_cup_data  # noqa: E402
OLYMPIC_DATA_FILE = (Path(__file__).resolve().parent
                     / 'test_data'/'tiny_olympic.csv')
WORLDCUP_DATA_FILE = (Path(__file__).resolve().parent
                      / 'test_data'/'tiny_worldcup.csv')


def test_medal_score(data: str) -> None:
    """
    test_medal_score takes in a path to tiny_olympic.csv
    It tests whether the medal_score column is correctly added
    to the dataframe, and if the math lines up with what we'd expect

    Parameters:
    data (str): String containing path to tiny_olympic.csv

    Returns:
    None
    """
    df = load_olympic_data(data)

    expected_scores = [9, 0, 20, 850]
    actual_scores = df['medal_score'].tolist()
    assert actual_scores == expected_scores


def test_game_type(data: str) -> None:
    """
    test_game_type takes in a path to tiny_olympic.csv
    It tests whether the games_type column is correctly added to the
    dataframe, and if the string extraction worked correctly to set it
    to the correct type of Olympic games

    Parameters:
    data (str): String containing path to tiny_olympic.csv

    Returns:
    None
    """
    df = load_olympic_data(data)
    expected_game_types = ['Summer', 'Winter', 'Summer', 'Winter']
    actual_game_types = df['games_type'].tolist()
    assert actual_game_types == expected_game_types


def test_worldcup_champion(data: str) -> None:
    """
    test_worldcup_champion takes in a path to tiny_worldcup.csv
    It tests whether the wc_score column is correctly added to the
    dataframe, and if the champion is correctly detected.

    Parameters:
    data (str): String containing path to tiny_worldcup.csv

    Returns:
    None
    """
    df = load_world_cup_data(data)

    wc_1930 = df[df['tournament_id'] == 'WC-1930']
    wc_1950 = df[df['tournament_id'] == 'WC-1950']
    # Checking champion correctly got points
    uruguay_1930 = wc_1930[wc_1930['team_name'] == 'Uruguay'].iloc[0]
    assert uruguay_1930['wc_score'] == 15

    # Checking runner up correctly did not get champion points
    argentina_1930 = wc_1930[wc_1930['team_name'] == 'Argentina'].iloc[0]
    assert argentina_1930['wc_score'] != 15

    uruguay_1950 = wc_1950[wc_1950['team_name'] == 'Uruguay'].iloc[0]
    assert uruguay_1950['wc_score'] == 15

    brazil_1950 = wc_1950[wc_1950['team_name'] == 'Brazil'].iloc[0]
    assert brazil_1950['wc_score'] != 15


def main():
    test_medal_score(OLYMPIC_DATA_FILE)
    test_game_type(OLYMPIC_DATA_FILE)

    test_worldcup_champion(WORLDCUP_DATA_FILE)


if __name__ == "__main__":
    main()
