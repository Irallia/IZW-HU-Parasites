# This code runs for about 10 minutes.

import csv
import itertools
from time import gmtime, strftime


def main():
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    print('-------------------')

    filepath = "../data/GloBI_Dump/interactions.tsv"
    freeliving_source = ["parasiteOf", "pathogenOf"]
    freeliving_target = ["hasParasite", "hasPathogen"]
    parasite_source = ["preysOn", "eats", "flowersVisitedBy", "hasPathogen", "pollinatedBy", "hasParasite", "hostOf"]
    parasite_target = ["preyedUponBy", "parasiteOf", "visitsFlowersOf", "pathogenOf", "hasHost"]
    #           [["ott_id","taxon_name"]]
    freelivings = []
    parasites = []
    SAME_AS = []
    freelivings_path = '../data/interaction_data/freelivings.csv' 
    parasites_path = '../data/interaction_data/parasites.csv' 

    index = 0
    no_ott_source = 0
    no_ott_target = 0

    with open(filepath, "r", encoding="utf8") as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        for row in reader:
            # print(row)
            # break
            index += 1
            interaction = row[10]
            if row[0] != '':
                if len(row[0].split(':')) < 2:
                    joined = ''.join(row[:6])
                    if joined.find('SAME_AS') != -1:
                        ott_index = row.index('SAME_AS') + 1
                        SAME_AS.append([row[10], row[ott_index], row[ott_index + 1]])
                    else:
                        no_ott_source += 1
                else:
                    ott = row[0].split(':')[1]
                    name = row[1]
                    if interaction in freeliving_source:
                        freelivings.append([ott, name])
                    elif interaction in parasite_source:
                        parasites.append([ott, name])
            if row[11] != '':
                if len(row[11].split(':')) < 2:
                    if ((''.join(row[10:15])).find('SAME_AS')) != -1:
                        print('target:', row[10:15])
                    no_ott_target += 1
                else:
                    ott = row[11].split(':')[1]
                    name = row[12]
                    if interaction in freeliving_target:
                        freelivings.append([ott, name])
                    elif interaction in parasite_target:
                        parasites.append([ott, name])

    print('-------------------')
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    print('-------------------')
    print('tsv_len =', index)
    print('no ott source:', no_ott_source)
    print('no ott target:', no_ott_target)

    print('number of freelivings:', len(freelivings))
    freelivings.sort()
    freelivings = list(freelivings for freelivings,_ in itertools.groupby(freelivings))
    print('number of freelivings:', len(freelivings), '(distinct)')
    
    print('number of parasites:', len(parasites))
    parasites.sort()
    parasites = list(parasites for parasites,_ in itertools.groupby(parasites))
    print('number of parasites:', len(parasites), '(distinct)')

    print('number of SAME_AS:', len(SAME_AS))
    SAME_AS.sort()
    SAME_AS = list(SAME_AS for SAME_AS,_ in itertools.groupby(SAME_AS))
    print('number of SAME_AS:', len(SAME_AS), '(distinct)')

    for item in SAME_AS:
        ott = item[1].split(':')[1]
        name = item[2]
        if item[0] in freeliving_source:
            freelivings.append([ott, name])
        elif item[0] in parasite_source:
            parasites.append([ott, name])

    freelivings.sort()
    freelivings = list(freelivings for freelivings,_ in itertools.groupby(freelivings))
    print('number of freelivings + SAME_AS:', len(freelivings), '(distinct)')
    
    parasites.sort()
    parasites = list(parasites for parasites,_ in itertools.groupby(parasites))
    print('number of parasites + SAME_AS:', len(parasites), '(distinct)')

    # -------------------------------------------------
    with open(freelivings_path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(freelivings)

    with open(parasites_path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(parasites)
    # -------------------------------------------------
    print('-------------------')
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    return

main()
