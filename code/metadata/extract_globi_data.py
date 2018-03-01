# This code runs for about 10 minutes.

import csv
import itertools
from time import gmtime, strftime

no_ott_source = 0
no_ott_target = 0

def main():
    global no_ott_source
    global no_ott_target
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    print('-------------------')

    filepath = "./data/GloBI_Dump/interactions.tsv"
    parasite_source = ["parasiteOf", "pathogenOf"]
    parasite_target = ["hasParasite", "hasPathogen"]
    freeliving_source = ["preysOn", "eats", "flowersVisitedBy", "hasPathogen", "pollinatedBy", "hasParasite", "hostOf"]
    freeliving_target = ["preyedUponBy", "parasiteOf", "visitsFlowersOf", "pathogenOf", "hasHost"]
    #           [["ott_id","taxon_name"]]
    freelivings = []
    parasites = []
    
    freelivings_path = './data/interaction_data/freelivings.csv' 
    parasites_path = './data/interaction_data/parasites.csv' 

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
                    print('no ott available')
                else:
                    ott = row[0].split(':')
                    name = row[1]
                    # normal case (otherwise no ott available, but maybe another one):
                    if len(ott) >= 2:
                        if interaction in freeliving_source:
                            freelivings.append([ott[1], name, interaction])
                        elif interaction in parasite_source:
                            parasites.append([ott[1], name, interaction])
            # -------------------------------- target? --------------------------------
            if any(interaction in target for target in (freeliving_target, parasite_target)):
                if row[11] == '' or not 'OTT' in  row[11]:
                    print('no ott available')
                else:
                    ott = row[11].split(':')
                    name = row[12]
                    # normal case (otherwise no ott available, but maybe another one):
                    if len(ott) >= 2:
                        if interaction in freeliving_target:
                            freelivings.append([ott[1], name, interaction])
                        elif interaction in parasite_target:
                            parasites.append([ott[1], name, interaction])

    print('-------------------')
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    print('-------------------')
    print('tsv_len =', index)
    print('no ott source:', no_ott_source)
    print('no ott target:', no_ott_target)

    freelivings = disambiguate_list(freelivings, 'freelivings')
    parasites = disambiguate_list(parasites, 'parasites')

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

def is_int(value):
    try: 
        int(value)
        return True
    except ValueError:
        return False

def disambiguate_list(current_list, name):
    print('number of', name, ':', len(current_list))
    current_list.sort()
    current_list = list(current_list for current_list,_ in itertools.groupby(current_list))
    print('number of', name, ':', len(current_list), '(distinct)')
    return current_list

main()
