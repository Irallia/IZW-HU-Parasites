import pandas as pd

ott_taxa = pd.read_csv('../data/interaction_data/ott_taxa.csv')
nodelist = pd.read_csv('../data/nodelist/Eukaryota.csv')
# nodelist = nodelist.dropna(axis=1)
merged = ott_taxa.merge(nodelist, on='ott_id')
merged.to_csv('../data/nodelist/Eukaryota-taxa.csv', index=False)
