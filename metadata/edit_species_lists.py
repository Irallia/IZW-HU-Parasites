import csv
import datetime
from copy import deepcopy
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored, cprint

from Helpers import print_time

path_parasites = "../data/interaction_data/parasites.csv"
path_freelivings = "../data/interaction_data/freelivings.csv"

# global variables:
START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)
freelivings = []
parasites = []
archaea_or_bacteria = 0
internal_parasite = 0
internal_freeliving = 0

def main():
    global START_TIME
    global CURRENT_TIME
    global freelivings
    global parasites
    global archaea_or_bacteria
    global internal_parasite
    global internal_freeliving

    print(colored("------------------------ edit species lists ------------------------", "green"))
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    CURRENT_TIME = print_time(START_TIME)

    print(colored("---------------- read parasites and freelivings ----------------", "green"))
    print("Freelivings:")
    freelivings = read_tags(path_freelivings)
    print("Parasites:")
    parasites = read_tags(path_parasites)
    CURRENT_TIME = print_time(CURRENT_TIME)

    print(colored("---------------- delete Archaea and Bacteria ----------------", "green"))
    subtree_names = ['Bacteria', 'Archaea']
    for item in subtree_names:
        print(item, ':')
        subtree_path = '../data/subtree/' + item + '.tre'
        tree = Phylo.read(subtree_path, 'newick')
        delete_archaea_or_bacteria(tree.clade)
        CURRENT_TIME = print_time(CURRENT_TIME)

    print(colored("---------------- delete internal Eukaryota ----------------", "green"))
    subtree_path = '../data/subtree/Eukaryota.tre'
    tree = Phylo.read(subtree_path, 'newick')
    delete_internal_nodes(tree.clade)

    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("--------------------------------", "green"))
            
    print(colored(archaea_or_bacteria, 'blue'), "archaea or bacteria found and deleted")
    print(colored(internal_freeliving, 'blue'), "internal freeliving tags found and", colored(internal_parasite, 'blue'), "internal parasite tags found and deleted")

    print("Freelivings:", len(freelivings))
    print("Parasites:", len(parasites))

     # -------------------------------------------------
    csv_title = '../data/interaction_data/reduced_freelivings.csv' 
    with open(csv_title, 'w') as species_file:
        writer = csv.writer(species_file, quoting=csv.QUOTE_ALL)
        writer.writerow(freelivings)
    csv_title = '../data/interaction_data/reduced_parasites.csv' 
    with open(csv_title, 'w') as species_file:
        writer = csv.writer(species_file, quoting=csv.QUOTE_ALL)
        writer.writerow(parasites)
    # -------------------------------------------------
    return

def read_tags(path):
    tag_array = []
    nr_tags = 0
    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if row != []:
                id_array = row[0]
                nr_tags += 1
                tag_array.append("ott" + id_array)
        print('number of tag:', nr_tags)
    return tag_array

def delete_archaea_or_bacteria(subtree):
    global freelivings
    global parasites
    global archaea_or_bacteria
    ott = subtree.name.split("$")[0] # remove index
    tag_boolf = get_tag(ott, freelivings)
    tag_boolp = get_tag(ott, parasites)
    freelivings = tag_boolf[1]
    parasites = tag_boolp[1] 

    if tag_boolp[0] or tag_boolf[0]:
        archaea_or_bacteria += 1

    if not subtree.is_terminal():
        for clade in subtree.clades:
            delete_archaea_or_bacteria(clade)
    return

def delete_internal_nodes(subtree):
    global freelivings
    global parasites
    global internal_parasite
    global internal_freeliving
    
    ott = subtree.name.split("$")[0] # remove index

    if not subtree.is_terminal():
        tag_boolf = get_tag(ott, freelivings)
        tag_boolp = get_tag(ott, parasites)
        freelivings = tag_boolf[1]
        parasites = tag_boolp[1] 
        
        if tag_boolf[0]:
            internal_freeliving += 1
        if tag_boolp[0]:
            internal_parasite += 1
        for clade in subtree.clades:
            delete_internal_nodes(clade)
    return

def get_tag(name, species_list):
    # Checks for the presence of name in any string in the list
    for item in species_list:
        # mrcaott_item = 'mrca' + item + 'ott'
        if item == name or name.endswith(item): # or name.startswith(mrcaott_item):
            species_list.remove(item)
            return [True, species_list]
        if not (name.startswith('mrca') or name.startswith('ott')):
            print(name)
    return [False, species_list]

main()
