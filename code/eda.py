from data_processor import (
    load_olympic_data,
    load_world_cup_data,
    load_gdp_data,
    load_gdp_per_capita_data,
    load_population_data
)
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from merging import merge_olympic_worldbank, merge_worldcup_worldbank
from pathlib import Path

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


def main():
    olympic_data = load_olympic_data(OLYMPICS_DATA_PATH)
    worldcup_data = load_world_cup_data(WORLD_CUP_DATA_PATH)
    gdp_data = load_gdp_data(GDP_DATA_PATH)
    gdp_pcap_data = load_gdp_per_capita_data(GDP_PCAP_DATA_PATH)
    pop_data = load_population_data(POP_DATA_PATH)

    merged_olympic = merge_olympic_worldbank(olympic_data,
                                             gdp_data,
                                             gdp_pcap_data,
                                             pop_data)

    merged_worldcup = merge_worldcup_worldbank(worldcup_data,
                                               gdp_data,
                                               gdp_pcap_data,
                                               pop_data)

    print("Olympic data size:" + str(olympic_data.shape))
    print("Worldcup data size:" + str(worldcup_data.shape))
    print("gdp data size:" + str(gdp_data.shape))
    print("gdp pcap data size:" + str(gdp_pcap_data.shape))
    print("pop data size:" + str(pop_data.shape))

    print("merged olympics size:" + str(merged_olympic.shape))
    print("merged worldcup size:" + str(merged_worldcup.shape))

    print(merged_olympic.isna().sum())

    print(merged_worldcup.isna().sum())

    print(merged_olympic[['medal_score',
                          'Population Value',
                          'GDP Value', 'GDP per Capita Value']].describe())

    print(merged_worldcup[['wc_score',
                           'Population Value',
                           'GDP Value', 'GDP per Capita Value']].describe())

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=merged_olympic, x='GDP Value',
                    y='medal_score')

    plt.xscale('log')

    plt.title('National Wealth vs. Olympic Performance')
    plt.xlabel('GDP (Log Scale)')
    plt.ylabel('Olympic Medal Score')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=merged_olympic, x='GDP per Capita Value',
                    y='medals_per_capita')

    plt.xscale('log')
    plt.title('Wealth Per Citizen vs. Medals Per Citizen')
    plt.xlabel('GDP per Capita (Log Scale)')
    plt.ylabel('Medals per Capita')
    plt.show()

    country_avg = merged_worldcup.groupby('country')['wc_score'].mean()
    country_gdp = (
        merged_worldcup.groupby('country')['GDP per Capita Value'].mean())

    combined = pd.concat([country_avg, country_gdp], axis=1)
    combined.dropna(subset=['GDP per Capita Value'], inplace=True)
    combined.sort_values(by='wc_score', ascending=False, inplace=True)

    plt.figure(figsize=(10, 12))
    sns.barplot(data=combined, y=combined.index, x='wc_score')
    plt.xlabel('Average World Cup Score')
    plt.ylabel('Country')
    plt.title('Top 20 Countries by Average World Cup Performance')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=merged_worldcup, x='GDP Value', y='wc_score')
    plt.xscale('log')
    plt.title('National Wealth vs. World Cup Performance')
    plt.xlabel('GDP (Log Scale)')
    plt.ylabel('World Cup Score')
    plt.show()

    print(merged_worldcup.shape)
    print(merged_olympic.shape)


if __name__ == "__main__":
    main()
