# This code runs for about 10 minutes.

import csv
import itertools
from time import gmtime, strftime


def main():
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    print('-------------------')

    filepath = "../data/opentree3.1_taxonomic_tree/taxonomy.tsv"
    #           [["ott_id", "taxon_name", "taxa", "uniqname"]]
    ott_taxa = []
    
    ott_taxa_path = '../data/interaction_data/ott_taxa.csv' 
    
    with open(filepath, "r", encoding="utf8") as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        for row in reader:
            uid = 'ott' + row['uid']
            name = row['name']
            rank = row['rank']
            uniqname = row['uniqname']
            ott_taxa.append([uid, name, rank, uniqname])

    print('-------------------')
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    print('-------------------')

    print('number of ott_taxa:', len(ott_taxa))
    
    # -------------------------------------------------
    with open(ott_taxa_path, "w", encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(['ott_id', 'name', 'rank', 'uniqname'])
        writer.writerows(ott_taxa)
    # -------------------------------------------------
    print('-------------------')
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    return

main()
