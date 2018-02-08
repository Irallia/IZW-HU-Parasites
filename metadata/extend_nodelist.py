import pandas as pd

ott_taxa = pd.read_csv('../data/interaction_data/ott_taxa.csv')
nodelist = pd.read_csv('../data/nodelist/Eukaryota-castor.csv')
# nodelist = nodelist.dropna(axis=1)
merged = ott_taxa.merge(nodelist, on='ott_id')
merged.to_csv('../results/Eukaryota-taxa.csv', index=False)
