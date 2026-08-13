"""

"""
from data_processor import (
    load_olympic_data,
    load_world_cup_data,
    load_gdp_data,
    load_gdp_per_capita_data,
    load_population_data
)
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
from merging import merge_olympic_worldbank, merge_worldcup_worldbank
from pathlib import Path
from scipy.stats import pearsonr
import numpy as np
from scipy.stats import linregress

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
    clean_olympic = merged_olympic.dropna(subset=['GDP Value', 'medal_score'])
    clean_olympic['decade'] = (clean_olympic['year'] // 10) * 10
    clean_worldcup = merged_worldcup.dropna(subset=['GDP Value',
                                                    'wc_score'])
    # RESULT: GDP Value vs medal_score: r=0.499907169442384,
    # p=9.504417653523219e-79
    test_correlation(clean_olympic, 'GDP Value', 'medal_score')
    # RESULT: GDP per Capita Value vs medals_per_capita: r=0.07850425600733467,
    # p=0.005874533330687652
    test_correlation(clean_olympic, 'GDP per Capita Value',
                     'medals_per_capita')

    # RESULT: log_GDP vs medal_score: r=0.45738197967698935,
    # p=1.285760176047609e-64
    clean_olympic['log_GDP'] = np.log(clean_olympic['GDP Value'])
    test_correlation(clean_olympic, 'log_GDP', 'medal_score')

    summer_olympic = clean_olympic[clean_olympic['games_type'] == 'Summer']
    winter_olympic = clean_olympic[clean_olympic['games_type'] == 'Winter']

    # RESULT: GDP Value vs medal_score: r=0.6804787725119179,
    # p=4.521076659505065e-124
    test_correlation(summer_olympic, 'GDP Value', 'medal_score')
    # RESULT: GDP Value vs medal_score: r=0.37207380354113273,
    # p=4.1411494734471195e-12
    test_correlation(winter_olympic, 'GDP Value', 'medal_score')
    # RESULT: GDP Value vs wc_score: r=0.2261855900544816,
    # p=3.1979074575783226e-07
    test_correlation(clean_worldcup, 'GDP Value', 'wc_score')

    result = linregress(clean_olympic['GDP per Capita Value'],
                        clean_olympic['medals_per_capita'])
    clean_olympic['predicted_medals'] = (
        result.slope * clean_olympic['GDP per Capita Value']
        + result.intercept
    )
    clean_olympic['diff'] = (clean_olympic['medals_per_capita'] -
                             clean_olympic['predicted_medals'])
    min_population = 1_000_000
    filterable = clean_olympic[clean_olympic['Population Value']
                               >= min_population]
    country_diffs_filtered = (filterable.groupby('country')['diff'].mean()
                              .sort_values(ascending=False))
    print(country_diffs_filtered.head(10))
    print(country_diffs_filtered.tail(10))

    print(clean_olympic[['year', 'decade']].head(10))
    print(sorted(clean_olympic['decade'].unique()))

    for decade in sorted(clean_olympic['decade'].unique()):
        decade_data = clean_olympic[clean_olympic['decade'] == decade]
        print(f'--- {decade}s (n={len(decade_data)}) ---')
        test_correlation(decade_data, 'GDP Value', 'medal_score')


def test_correlation(df, x_col, y_col):
    r, p_value = pearsonr(df[x_col], df[y_col])
    print(f'{x_col} vs {y_col}: r={r}, p={p_value}')
    return r, p_value


if __name__ == "__main__":
    main()
