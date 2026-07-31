from data_processor import (
    load_olympic_data,
    load_world_cup_data,
    load_gdp_data,
    load_gdp_per_capita_data,
    load_population_data
)

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


if __name__ == "__main__":
    main()
