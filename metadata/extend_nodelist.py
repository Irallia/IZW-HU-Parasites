import pandas as pd
# https://pandas.pydata.org/pandas-docs/stable/merging.html
# We do an SQL LEFT OUTER JOIN.

ott_taxa = pd.read_csv('../data/interaction_data/ott_taxa.csv', encoding='utf-8')
nodelist = pd.read_csv('../data/nodelist/Eukaryota-castor.csv', encoding='utf-8')
merged = pd.merge(nodelist, ott_taxa, how='left', on='ott_id')

print(len(nodelist),'merge', len(ott_taxa), '->', len(merged))
print('castor results added')

kingdom_mapping = pd.read_csv('../data/nodelist/Eukaryota-kingdom_mapping.csv', encoding='utf-8')
merged = pd.merge(merged, kingdom_mapping, how='left', on='ott_id')

print('merge', len(kingdom_mapping))
print('kingdom taxa added')

phylum_mapping = pd.read_csv('../data/nodelist/Eukaryota-phylum_mapping.csv', encoding='utf-8')
merged = pd.merge(merged, phylum_mapping, how='left', on='ott_id')

print('merge', len(phylum_mapping))
print('phylum taxa added')

class_mapping = pd.read_csv('../data/nodelist/Eukaryota-class_mapping.csv', encoding='utf-8')
merged = pd.merge(merged, class_mapping, how='left', on='ott_id')

print('merge', len(class_mapping))
print('class taxa added')

order_mapping = pd.read_csv('../data/nodelist/Eukaryota-order_mapping.csv', encoding='utf-8')
merged = pd.merge(merged, order_mapping, how='left', on='ott_id')
merged.to_csv('../results/Eukaryota-taxa-new-new.csv', index=False, encoding='utf-8')

print('merge', len(order_mapping))
print('order taxa added')