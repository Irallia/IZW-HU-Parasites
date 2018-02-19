# delete 100 random lines ...

import csv
import datetime
import sys
from copy import deepcopy
from random import shuffle
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored, cprint

from Helpers import print_time

# input arguments
args = sys.argv

# values for simulation:
index = sys.argv[1]
border = int(sys.argv[2])

path_freelivings = "../data/interaction_data/freelivings.csv"
path_parasites = "../data/interaction_data/parasites.csv"

# global variables:
START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)
freelivings = []
parasites = []
nr_leave_nodes = 0
nr_used_freelivings = 0
nr_used_parasites = 0
unknown = 0
doubleTagged = 0
nodelist = []

def main():
    global START_TIME
    global CURRENT_TIME
    global freelivings
    global parasites
    global nr_leave_nodes
    global nr_used_freelivings
    global nr_used_parasites
    global unknown
    global nodelist
    global doubleTagged

    global index
    global border

    print(colored("------------------------ build nodelists ------------------------", "green"))
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    CURRENT_TIME = print_time(START_TIME)

    print(colored("---------------- read parasites and freelivings ----------------", "green"))
    print("Freelivings:")
    freelivings = read_tags(path_freelivings)
    print("Parasites:")
    parasites = read_tags(path_parasites)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- read tree ----------------", "green"))
    subtree_path = '../data/subtree/Eukaryota.tre'
    print("Build nodelist for: Eukaryota")
    tree = Phylo.read(subtree_path, 'newick')
    print(colored("---------------- tag tree ----------------", "green"))
    shuffle(freelivings)
    shuffle(parasites)
    i = 0
    while i < border:
        freelivings.pop()
        parasites.pop()
        i += 1

    fill_tree_with_tags(tree.clade, index)
    print(colored(nr_leave_nodes, 'blue'), "leave nodes are in the tree")
    print(colored(nr_used_freelivings, 'blue'), "freeliving tags were used,", colored(nr_used_parasites, 'blue'), "parasite tags were used =>", colored(unknown, 'blue'), "unknown leave nodes")
    print("Rootnode, Originaltag, Finaltag, Nr_children")
    print(nodelist[0])
    print(doubleTagged, "are tagged as P, but could also be FL!")
    # ---- reset countings ----
    nr_leave_nodes = 0
    nr_used_freelivings = 0
    nr_used_parasites = 0
    unknown = 0
    nodelist = []
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("--------------------------------", "green"))
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

def fill_tree_with_tags(subtree, index):
    global nr_leave_nodes
    global nr_used_freelivings
    global nr_used_parasites
    global unknown
    global nodelist
    global doubleTagged
    
    ott = subtree.name.split("$")[0] # remove index
    #              0    1       2
    # nodelist - [id, originaltag, finaltag]
    nodelist.append([ott, "", ""])
    current_list_index = len(nodelist) - 1

    if subtree.is_terminal():
        nr_leave_nodes += 1
        tag_boolp = get_tag(ott, 'P')
        if tag_boolp:
            nr_used_parasites += 1
            nodelist[current_list_index][1] = "2"
            if (get_tag(ott, 'FL')):
                doubleTagged += 1
        else:
            tag_boolf = get_tag(ott, 'FL')
            if tag_boolf:
                nr_used_freelivings += 1
                nodelist[current_list_index][1] = "1"
            else:
                nodelist[current_list_index][1] = "NA"
                unknown += 1
    else:
        for clade in subtree.clades:
            fill_tree_with_tags(clade, index)
    # -------------------------------------------------
    csv_title = '../data/evaluation/Eukaryota'+ index + '-' + str(border) +'.csv' 
    nodelist_file = open(csv_title, 'a')
    writer = csv.writer(nodelist_file)
    writer.writerow((nodelist[current_list_index])) 
    nodelist_file.close()
    # -------------------------------------------------
    return

def get_tag(name, tag):
    global freelivings
    global parasites
    if tag == 'FL':
        species_list = freelivings
    else:
        species_list = parasites
    # Checks for the presence of name in any string in the list
    for item in species_list:
        # mrcaott_item = 'mrca' + item + 'ott'
        if item == name or name.endswith(item): # or name.startswith(mrcaott_item):
            species_list.remove(item)
            return True
    return False

main()
