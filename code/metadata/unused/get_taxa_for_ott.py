# This code runs for about 10 minutes.

import csv
import itertools
from time import gmtime, strftime

SAME_AS = []

def main():
    global SAME_AS
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    print('-------------------')

    filepath = "../data/GloBI_Dump/interactions.tsv"
    #           [["ott_id", "taxon_name", "taxa"]]
    ott_taxa_matching = []
    
    ott_taxa_matching_path = '../data/interaction_data/ott_taxa_matching.csv' 

    index = 0

    with open(filepath, "r", encoding="utf8") as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        for row in reader:            
            # -------------------------------- source --------------------------------
            if row[0] == '' or not 'OTT' in row[0]:
                get_same_as_ott(row, 'source')
            else:
                ott = row[0].split(':')
                name = row[1]
                taxa = row[2]
                # no ott available, but maybe another one:
                if len(ott) < 2:
                    get_same_as_ott(row, 'source')
                # normal case:
                else:
                    ott_taxa_matching.append([ott[1], name, taxa])
            # -------------------------------- target --------------------------------
                
            if row[11] == '' or not 'OTT' in  row[11]:
                get_same_as_ott(row, 'target')
            else:
                ott = row[11].split(':')
                name = row[12]
                taxa = row[13]
                # no ott available, but maybe another one:
                if len(ott) < 2:
                    get_same_as_ott(row, 'target')
                # normal case:
                else:
                    ott_taxa_matching.append([ott[1], name, taxa])

    print('-------------------')
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    print('-------------------')
    print('tsv_len =', index)

    print('number of ott_taxa_matching:', len(ott_taxa_matching))
    ott_taxa_matching.sort()
    ott_taxa_matching = list(ott_taxa_matching for ott_taxa_matching,_ in itertools.groupby(ott_taxa_matching))
    print('number of ott_taxa_matching:', len(ott_taxa_matching), '(distinct)')
    
    print('number of SAME_AS:', len(SAME_AS))
    SAME_AS.sort()
    SAME_AS = list(SAME_AS for SAME_AS,_ in itertools.groupby(SAME_AS))
    print('number of SAME_AS:', len(SAME_AS), '(distinct)')

    for item in SAME_AS:
        ott = item[0].split(':')[1]
        name = item[1]
        taxa = item[2]
        ott_taxa_matching.append([ott, name, taxa])

    ott_taxa_matching.sort()
    ott_taxa_matching = list(ott_taxa_matching for ott_taxa_matching,_ in itertools.groupby(ott_taxa_matching))
    print('number of ott_taxa_matching + SAME_AS:', len(ott_taxa_matching), '(distinct)')

    # -------------------------------------------------
    with open(ott_taxa_matching_path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(ott_taxa_matching)
    # -------------------------------------------------
    print('-------------------')
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    return

def get_same_as_ott(row, st):
    global SAME_AS
    if st =='source':
        global no_ott_source
        if 'SAME_AS' in row[:10]:
            ott_index = row.index('SAME_AS') + 1
            if not is_int(row[ott_index].split(':')[1]):
                return
            SAME_AS.append([row[ott_index], row[ott_index + 1], row[ott_index + 2]])
    if st =='target':
        global no_ott_target
        if 'SAME_AS' in row[10:]:
            ott_index = row.index('SAME_AS') + 1
            if not is_int(row[ott_index].split(':')[1]):
                return
            SAME_AS.append([row[ott_index], row[ott_index + 1], row[ott_index + 2]])
    return

def is_int(value):
    try: 
        int(value)
        return True
    except ValueError:
        return False

main()
