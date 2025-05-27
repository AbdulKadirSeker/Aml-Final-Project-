import os
from pathlib import Path
import pandas as pd
import numpy as np
from functools import reduce
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import matplotlib.pyplot as plt

# --- Paths ---
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


# --- Data Loading ---
def load_csv(name: str) -> pd.DataFrame:
    """
    Load a CSV file from the data directory by name (without extension).
    Example: load_csv('players') reads 'data/players.csv'.
    """
    path = DATA_DIR / f"{name}.csv"
    return pd.read_csv(path)


# Convenience functions for each file
def load_appearances(): return load_csv('appearances')


def load_club_games(): return load_csv('club_games')


def load_clubs(): return load_csv('clubs')


def load_competitions():     return load_csv('competitions')


def load_game_events(): return load_csv('game_events')


def load_game_lineups(): return load_csv('game_lineups')


def load_games(): return load_csv('games')


def load_player_valuations(): return load_csv('player_valuations')


def load_players(): return load_csv('players')


def load_transfers(): return load_csv('transfers')


def load_all() -> dict[str, pd.DataFrame]:
    """
    Load every .csv file in your data directory into a dict of DataFrames.
    Keys are the filename without extension.
    """
    data = {}
    for fp in DATA_DIR.glob("*.csv"):
        key = fp.stem
        data[key] = pd.read_csv(fp)
    return data


# --- Merge Helpers ---
def merge_two(df1: pd.DataFrame, df2: pd.DataFrame, on: str, how: str = 'left') -> pd.DataFrame:
    """Merge two DataFrames on a key."""
    return df1.merge(df2, on=on, how=how)


def merge_multiple(dfs: list, on: str, how: str = 'left') -> pd.DataFrame:
    """Sequentially merge a list of DataFrames on a key."""
    return reduce(lambda left, right: left.merge(right, on=on, how=how), dfs)


# --- Feature Engineering ---
def aggregate_player_stats(appearances: pd.DataFrame) -> pd.DataFrame:
    return (appearances
            .groupby('player_id')
            .agg(n_games=('game_id', 'count'),
                 total_yellow=('yellow_cards', 'sum'),
                 total_red=('red_cards', 'sum'))
            .reset_index())


def get_latest_valuation(vals: pd.DataFrame) -> pd.DataFrame:
    vals['date'] = pd.to_datetime(vals['date'])
    idx = vals.groupby('player_id')['date'].idxmax()
    return vals.loc[idx, ['player_id', 'market_value_in_eur']].reset_index(drop=True)


def merge_player_data(players, stats, latest_valuations):
    """
    Joins players with their aggregated stats and latest market valuation.
    """
    df = players.merge(stats, on='player_id', how='left')
    df = df.merge(latest_valuations[['player_id', 'market_value_in_eur']], on='player_id', how='left')
    return df


# --- Preprocessing ---
def fillna_and_scale(df: pd.DataFrame, cols: list) -> tuple:
    df = df.copy()
    df[cols] = df[cols].fillna(0)
    scaler = StandardScaler()
    return scaler.fit_transform(df[cols]), scaler


def encode_categorical(df: pd.DataFrame, cols: list) -> tuple:
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    arr = encoder.fit_transform(df[cols])
    df_enc = pd.DataFrame(arr, columns=encoder.get_feature_names_out(cols), index=df.index)
    return df_enc, encoder


# --- Plotting ---
def plot_distribution(vals, title='Distribution', bins=50):
    plt.hist(vals, bins=bins)
    plt.title(title)
    plt.show()


def scatter_actual_vs_pred(y_true, y_pred, title='Actual vs Predicted'):
    plt.scatter(y_true, y_pred, alpha=0.5)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--')
    plt.title(title)
    plt.show()


# --- Age Computation ---
def compute_age(df, date_col = 'date_of_birth', ref_date = '2025-05-27'):
    df_copy = df.copy()
    # Parse birth dates, coercing invalid entries to NaT
    birth = pd.to_datetime(df[date_col], errors='coerce')
    # Determine reference date
    if ref_date is None:
        today = pd.Timestamp.today()
    else:
        today = pd.to_datetime(ref_date)
    # Calculate year difference
    years = today.year - birth.dt.year
    # Determine if each birthday has occurred this year
    had_birthday = (today.month > birth.dt.month) | \
                   ((today.month == birth.dt.month) & (today.day >= birth.dt.day))
    # Compute age, subtracting 1 where birthday hasn't occurred
    age = years - (~had_birthday).astype(pd.Int64Dtype())
    # Ensure Int64 dtype and preserve NaT as <NA>
    df_copy['age'] = age.astype(pd.Int64Dtype())
    return df_copy

# def compute_age(df):
#     #yyyy-mm-dd
#     ages = []
#     counter = 0
#     for i in df['date_of_birth']:
#         if i == 'NaN':
#             print('Computer lost')
#             break
#         print(f'{counter}: {i[:4]}')
#         counter += 1


# --- Pipeline Example ---
def prepare_main_player_dataframe() -> pd.DataFrame:
    players = load_players()
    appearances = load_appearances()
    valuations = load_player_valuations()
    stats = aggregate_player_stats(appearances)
    latest = get_latest_valuation(valuations)
    return merge_tables(players, merge_tables(stats, latest, 'player_id'), 'player_id')

