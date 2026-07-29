import pandas as pd

wc_weights = {
    'group stage': 1,
    'second group stage': 2,
    'round of 16': 4,
    'quarter-finals': 6,
    'quarter-final': 6,
    'semi-finals': 8,
    'semi-final': 8,
    'third-place match': 8,
    'final round': 10,
    'final': 12,
    'champ': 15
}


def load_olympic_data(data: str) -> pd.DataFrame:
    """
    Loads Olympic results data from a CSV file
    and calculates medal scores and game types

    Parameters:
    data (str): Path to the CSV file containing Olympic results data

    returns:
    pd.DataFrame: A DataFrame containing the Olympic results data
    """
    df = pd.read_csv(data)

    df['medal_score'] = (
        df['gold'] * 5
        + df['silver'] * 3
        + df['bronze'] * 1
    )

    df['games_type'] = df['edition'].apply(
        lambda e: 'Winter' if 'Winter' in e else 'Summer'
    )

    return df


def load_world_cup_data(data: str) -> pd.DataFrame:
    """
    Loads World Cup results data from a CSV file
    and calculates match points and World Cup scores

    Determines the champion of each tournament
    and assigns weights depending on the stage of the tournament

    Parameters:
    data (str): Path to the CSV file containing World Cup results data

    Returns:
    pd.DataFrame: A DataFrame containing the World Cup results data
    """
    df = pd.read_csv(data)

    df['match_points'] = df['win'] * 3 + df['draw'] * 1

    final_games = df[df['stage_name'].isin(['final', 'final round'])]

    total_points = final_games.groupby(['tournament_id', 'team_name']).apply(
        lambda x: x['match_points'].sum()
    )

    champs = total_points.groupby('tournament_id').idxmax().apply(
        lambda x: x[1]
        )

    df['wc_score'] = df['stage_name'].map(wc_weights)
    champs_df = champs.reset_index(name='champion_team')

    df = df.merge(champs_df, on='tournament_id', how='left')

    is_champ = df['team_name'] == df['champion_team']
    is_final_stage = df['stage_name'].isin(['final', 'final round'])
    df.loc[is_champ & is_final_stage, 'wc_score'] = 15

    best_rows = df.groupby(['tournament_id', 'team_name'])['wc_score'].idxmax()

    result = df.loc[best_rows]

    return result


def load_fwc_mens(data: str) -> pd.DataFrame:
    """
    Loads FIFA World Cup results data for men's
    tournaments only

    Parameters:
    data (str): Path to the CSV file containing World Cup results data

    Returns:
    pd.DataFrame: A DataFrame containing the men's World Cup
    results data
    """

    all_results = load_world_cup_data(data)

    filtered_results = all_results[all_results['tournament_name']
                                   .str.contains("Men's")]

    return filtered_results


def load_fwc_womens(data: str) -> pd.DataFrame:
    """
    Loads FIFA World Cup results data for women's
    tournaments only

    Parameters:
    data (str): Path to the CSV file containing World Cup results data

    Returns:
    pd.DataFrame: A DataFrame containing the women's World Cup
    results data
    """

    all_results = load_world_cup_data(data)

    filtered_results = all_results[all_results['tournament_name']
                                   .str.contains("Women's")]

    return filtered_results


def load_worldbank_data(data: str, val_name: str) -> pd.DataFrame:
    """
    Loads GDP data from a CSV file

    Parameters:
    data (str): Path to the CSV file containing GDP data

    Returns:
    pd.DataFrame: A DataFrame containing the GDP data
    """
    df = pd.read_csv(data, skiprows=4)

    year_cols = [c for c in df.columns if c.isdigit()]

    long_df = df.melt(
        id_vars=['Country Name', 'Country Code'],
        value_vars=year_cols,
        var_name='Year',
        value_name=val_name,
    )

    long_df['Year'] = long_df['Year'].astype(int)

    return long_df


def load_gdp_data(data: str) -> pd.DataFrame:
    return load_worldbank_data(data, 'GDP Value')


def load_gdp_per_capita_data(data: str) -> pd.DataFrame:
    return load_worldbank_data(data, 'GDP per Capita Value')


def load_population_data(data: str) -> pd.DataFrame:
    return load_worldbank_data(data, 'Population Value')
