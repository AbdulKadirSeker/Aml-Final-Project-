import pandas as pd
import os
from pathlib import Path
def load_one(folderpath,filename):
    fullpath = os.path.join(folderpath, filename)
    df = pd.read_csv(fullpath)
    return df
def load_all(folderpath):
    dfs = {}
    for fname in os.listdir(folderpath):
        full = os.path.join(folderpath, fname)
        if fname.endswith('.csv.gz'):
            key = fname[:-7]          # “players.csv.gz” → “players”
            comp = 'gzip'
        elif fname.endswith('.csv'):
            key = fname[:-4]          # “teams.csv” → “teams”
            comp = None
        else:
            continue                  # skip non‐CSV

        dfs[key] = pd.read_csv(full, compression=comp)

    return dfs

def merge_tables(t1, t2, t_id):
    return t1.merge(t2, on=t_id, how='left')


folder = "../Data"
df = load_all(folder)
print('Players_Table:\n',df['players'].head())
print('\n\n\n')
print('Player_Valuations:\n',df['player_valuations'].head())
print('\n\n\n')
print('Merged_Tables:\n',merge_tables(df['players'],df['player_valuations'],'player_id').head())
