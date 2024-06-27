# import standard packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def format_targetome_data(file):
    df = pd.read_excel(file, engine="openpyxl")
    df_full = df[["Entry", "BestRanked", "Chain_id"]]
    df_full['Chain_id'] = df_full['Chain_id'].str.replace("[\[\]']", "", regex=True)
    # Get the first letter shown
    df_full['Chain_id'] = df_full['Chain_id'].str.split(',').str[0].str.strip()
    # Rename BestRanked:PDB and Chain_id: chain
    df_full = df_full.rename(columns={"BestRanked": "PDB", "Chain_id": "chain"})
    return df_full

# function to get and format affinities properly
def format_aff(file):
    with open(file, 'r') as file:
        data = file.read()
    # Splitting the data into lines
    lines = data.strip().split("\n")
    pdb_names = [line.split("/")[1].split(".pdb")[0] for line in lines if ".pdb/log.log" in line]
    # affinity scores
    scores = [list(map(float, line.split()[2:])) for line in lines]
    # Creating a DataFrame
    df = pd.DataFrame({
        'PDB': pdb_names,
        'Score1': [score[0] for score in scores],
        'Score2': [score[1] for score in scores],
        'Score3': [score[2] for score in scores]
    })
    df['chain'] = df['PDB'].str.split('_').str[1].str[0]
    df['PDB'] = df['PDB'].str.replace(r'_.', '', regex=True)
    df_selected = df[['PDB', 'chain', 'Score1']]
    # complete set is 6621
    df_aff = df_selected
    df_aff = df_aff.rename(columns={"Score1": "affinity"})
    return df_aff
def merge_datasets(target_df, aff_df):
    # Merge to the two datasets - so we can get the uniprot ID of one dataset mathc up to the PDB of another
    merged_df = target_df.merge(aff_df, on=["PDB", "chain"], how="outer")
    merged_df = merged_df[merged_df['affinity'].notna()]
    sorted_df = merged_df.iloc[np.argsort(np.abs(merged_df['affinity'].values))[::-1]]
    return sorted_df

def prepare_data(targetome_file, affinity_file):
    target_df = format_targetome_data(targetome_file)
    aff_df = format_aff(affinity_file)
    sorted_df = merge_datasets(target_df, aff_df)
    return sorted_df
# # import file
# targetome_file = "Data.xlsx"
# affinity_file = "BAP_affinities.txt"
#
# df = prepare_data(targetome_file, affinity_file)
# print(df)