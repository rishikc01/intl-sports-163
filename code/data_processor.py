import pandas as pd

def load_olympic_data(data):
    df = pd.read_csv(data)

    df['medal_score'] = df['gold'] * 5 + df['silver'] * 3 + df['bronze'] * 1

    df['games_type'] = df['edition'].apply(lambda e: 'Winter' if 'Winter' in e else 'Summer')

    return df