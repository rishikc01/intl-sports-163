from pathlib import Path
import pandas as pd

from data_processor import (
    # load_fwc_mens,
    # load_fwc_womens,
    load_olympic_data,
    load_gdp_data,
    # load_gdp_percap_data,
    # load_pop_data
)

ROOT = Path(__file__).resolve().parent.parent
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
    "West Germany": "Germany"
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
    return merge_with_worldbank(olympic_data, gdp_data,
                                gdp_pcap_data, pop_data)


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


def main():
    olympic_countries = load_olympic_data(OLYMPICS_DATA_PATH)
    olympic_countries = set(olympic_countries['country']
                            .apply(standardize_country).unique())

    gdp_data = load_gdp_data(GDP_DATA_PATH)
    gdp_countries = set(gdp_data['Country Name'])

    print(olympic_countries - gdp_countries)


main()
