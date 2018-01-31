# This code runs for about 10 minutes.

import csv
import itertools
from time import gmtime, strftime

no_ott_source = 0
no_ott_target = 0
SAME_AS = []

def main():
    global no_ott_source
    global no_ott_target
    global SAME_AS
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
    
    freelivings_path = '../data/interaction_data/freelivings.csv' 
    parasites_path = '../data/interaction_data/parasites.csv' 

    index = 0

    with open(filepath, "r", encoding="utf8") as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        for row in reader:
            index += 1
            interaction = row[10]

            # eliminate useless interactions
            # -------------------------------- source? --------------------------------
            if any(interaction in source for source in (freeliving_source, parasite_source)):
                if row[0] == '' or not 'OTT' in row[0]:
                    get_same_as_ott(row, 'source')
                else:
                    ott = row[0].split(':')
                    name = row[1]
                    # no ott available, but maybe another one:
                    if len(ott) < 2:
                        get_same_as_ott(row, 'source')
                    # normal case:
                    else:
                        if interaction in freeliving_source:
                            freelivings.append([ott[1], name])
                        elif interaction in parasite_source:
                            parasites.append([ott[1], name])
            # -------------------------------- target? --------------------------------
            if any(interaction in target for target in (freeliving_target, parasite_target)):
                ott = row[0].split(':')
                name = row[1]
                if row[11] == '' or not 'OTT' in  row[11]:
                    get_same_as_ott(row, 'target')
                else:
                    # no ott available, but maybe another one:
                    if len(ott) < 2:
                        get_same_as_ott(row, 'target')
                    # normal case:
                    else:
                        if interaction in freeliving_target:
                            freelivings.append([ott[1], name])
                        elif interaction in parasite_target:
                            parasites.append([ott[1], name])

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

def get_same_as_ott(row, st):
    global SAME_AS
    if st =='source':
        global no_ott_source
        if 'SAME_AS' in row[:10]:
            ott_index = row.index('SAME_AS') + 1
            if not is_int(row[ott_index].split(':')[1]):
                return
            SAME_AS.append([row[10], row[ott_index], row[ott_index + 1]])
        else:
            no_ott_source += 1
    if st =='target':
        global no_ott_target
        if 'SAME_AS' in row[10:]:
            ott_index = row.index('SAME_AS') + 1
            if not is_int(row[ott_index].split(':')[1]):
                return
            SAME_AS.append([row[10], row[ott_index], row[ott_index + 1]])
        else:
            no_ott_target += 1
    return

def is_int(value):
    try: 
        int(value)
        return True
    except ValueError:
        return False

main()
