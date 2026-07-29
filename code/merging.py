from pathlib import Path

from data_processor import (
    load_fwc_mens,
    load_fwc_womens,
    load_olympic_data,
    load_gdp_data,
)

ROOT = Path(__file__).resolve().parent.parent
OLYMPICS_DATA_PATH = ROOT/'data'/'Olympic_Medal_Tally_History.csv'
GDP_DATA_PATH = ROOT/'data'/'gdp_data'/'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_234.csv'


# Country names are represented differently in the different datasets
# This is a map to standarize the country names across the datasets
country_mapping = {
    'Great Britain': 'United Kingdom',
    'Republic of Korea': 'Korea, Rep.',
    "Democratic People's Republic of Korea": "Korea, Dem. People’s Rep.",
    "People's Rebublic of China": "China",
    "Côte d'Ivoire": "Cote d'Ivoire",
    'Türkiye': 'Turkiye',
    'Vietnam': 'Viet Nam'
}


def main():
    olympic_countries = load_olympic_data(OLYMPICS_DATA_PATH)
    olympic_countries = set(olympic_countries['country'].unique())

    gdp_data = load_gdp_data(GDP_DATA_PATH)
    gdp_countries = set(gdp_data['Country Name'])

    print(olympic_countries - gdp_countries)


main()
