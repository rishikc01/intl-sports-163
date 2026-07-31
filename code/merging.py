"""
This file implements 4 total functions for standardizing country names
and merging Olympic and World Cup datasets with World Bank GDP,
GDP per capita, and population data.

standardize_country maps inconsistent country names across the sports and
World Bank datasets so merges join on a single normalized country value.

merge_with_worldbank is a generic merge helper used by the Olympic and
World Cup merge functions.

merge_olympic_worldbank merges Olympic results with World Bank data and
calculates medals per capita using population.

merge_worldcup_worldbank merges World Cup results with World Bank data.
"""

from pathlib import Path
import pandas as pd

# I had to look this up because I couldn't figure out an easy way to do this
ROOT = Path(__file__).resolve().parent.parent
WORLD_CUP_DATA_PATH = ROOT/'data'/'team_appearances.csv'
OLYMPICS_DATA_PATH = ROOT/'data'/'Olympic_Medal_Tally_History.csv'
GDP_DATA_PATH = (ROOT/'data' /
                 'gdp_data'/'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_234.csv')
GDP_PCAP_DATA_PATH = (ROOT/'data' /
                      'gdp_percap_data' /
                      'API_NY.GDP.PCAP.CD_DS2_en_csv_v2_33610.csv')
POP_DATA_PATH = (ROOT/'data' /
                 'pop_data' / 'API_SP.POP.TOTL_DS2_en_csv_v2_33112.csv')

# Country names are represented differently in the different datasets
# This is a map to standarize the country names across the datasets
country_mapping = {
    'Great Britain': 'United Kingdom',
    'Republic of Korea': 'Korea, Rep.',
    "Democratic People's Republic of Korea": "Korea, Dem. People's Rep.",
    "People's Republic of China": "China",
    "Côte d'Ivoire": "Cote d'Ivoire",
    'Türkiye': 'Turkiye',
    'Vietnam': 'Viet Nam',
    'Egypt': "Egypt, Arab Rep.",
    'Venezuela': "Venezuela, RB",
    'Islamic Republic of Iran': "Iran, Islamic Rep.",
    "The Bahamas": "Bahamas, The",
    "Republic of Moldova": "Moldova",
    "United Republic of Tanzania": "Tanzania",
    "Kingdom of Saudi Arabia": "Saudi Arabia",
    "Hong Kong, China": "Hong Kong SAR, China",
    "Kyrgyzstan": "Kyrgyz Republic",
    "Slovakia": "Slovak Republic",
    "ROC": "Russian Federation",
    # Historically in sports West Germany's accompishments
    # are counted towards Germany's total, so we will combine in this instance
    "West Germany": "Germany",

    # World Cup Mappings

    'South Korea': 'Korea, Rep.',
    'North Korea': "Korea, Dem. People's Rep.",
    'Ivory Coast': "Cote d'Ivoire",
    'Iran': 'Iran, Islamic Rep.',
    'Turkey': 'Turkiye',
    'Russia': 'Russian Federation',
    'Republic of Ireland': 'Ireland',
    'Czech Republic': 'Czechia',

    # In the World Cup, England Scotland, Wales, and Northern Ireland
    # compete as separate teams, but in the World Bank data they are all
    # represented as the United Kingdom. For the purposes of this project,
    #  we will combine them under the United Kingdom

    "England": "United Kingdom",
    "Scotland": "United Kingdom",
    "Wales": "United Kingdom",
    "Northern Ireland": "United Kingdom"
}


def standardize_country(name: str) -> str:
    return country_mapping.get(name, name)


def merge_with_worldbank(sport_data: pd.DataFrame,
                         gdp_data: pd.DataFrame,
                         gdp_pcap_data: pd.DataFrame,
                         pop_data: pd.DataFrame) -> pd.DataFrame:
    """
    Generic function to merge sports data with the three
    World Bank Datasets (GDP, GDP per capita, and population)
    based on country and year

    This function is called by the merge_olympic_worldbank
    and merge_worldcup_worldbank functions

    Parameters:
    sport_data (pd.DataFrame): DataFrame containing sports data
    gdp_data (pd.DataFrame): DataFrame containing GDP data
    gdp_pcap_data (pd.DataFrame): DataFrame containing GDP per capita data
    pop_data (pd.DataFrame): DataFrame containing population data

    Returns:
    pd.DataFrame: A DataFrame containing the merged data
    """
    if 'team_name' in sport_data.columns:
        sport_data = (sport_data.rename(columns={'team_name': 'country'}))

    sport_data['country'] = (sport_data['country']
                             .apply(standardize_country))

    merged_df = pd.merge(
        sport_data,
        gdp_data,
        left_on=['country', 'year'],
        right_on=['Country Name', 'Year'],
        how='left'
    )
    merged_df = merged_df.drop(
        columns=['Country Name', 'Country Code', 'Year'])

    merged_df = pd.merge(
        merged_df,
        gdp_pcap_data,
        left_on=['country', 'year'],
        right_on=['Country Name', 'Year'],
        how='left'
    )
    merged_df = merged_df.drop(
        columns=['Country Name', 'Country Code', 'Year'])

    merged_df = pd.merge(
        merged_df,
        pop_data,
        left_on=['country', 'year'],
        right_on=['Country Name', 'Year'],
        how='left'
    )
    merged_df = merged_df.drop(
        columns=['Country Name', 'Country Code', 'Year'])

    return merged_df


def merge_olympic_worldbank(olympic_data, gdp_data, gdp_pcap_data, pop_data):
    """
    Merges Olympic data with the three
    World Bank datasets

    Parameters:
    olympic_data (pd.DataFrame): DataFrame containing Olympic data
    gdp_data (pd.DataFrame): DataFrame containing GDP data
    gdp_pcap_data (pd.DataFrame): DataFrame containing GDP per capita data
    pop_data (pd.DataFrame): DataFrame containing population data

    Returns:
    pd.DataFrame: A DataFrame containing the merged data
    """
    merged_df = merge_with_worldbank(olympic_data, gdp_data,
                                     gdp_pcap_data, pop_data)

    merged_df["medals_per_capita"] = (
        merged_df["medal_score"] / merged_df["Population Value"]
    ) * 1_000_000

    return merged_df


def merge_worldcup_worldbank(worldcup_data, gdp_data, gdp_pcap_data, pop_data):
    """
    Merges World Cup data with the three
    World Bank datasets

    Parameters:
    worldcup_data (pd.DataFrame): DataFrame containing World Cup data
    gdp_data (pd.DataFrame): DataFrame containing GDP data
    gdp_pcap_data (pd.DataFrame): DataFrame containing GDP per capita data
    pop_data (pd.DataFrame): DataFrame containing population data

    Returns:
    pd.DataFrame: A DataFrame containing the merged data
    """
    return merge_with_worldbank(worldcup_data, gdp_data,
                                gdp_pcap_data, pop_data)
