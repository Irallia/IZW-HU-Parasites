import csv
import datetime
from copy import deepcopy
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored, cprint

from Helpers import print_time

path_freelivings = "../data/interaction_data/reduced_freelivings.csv"
path_parasites = "../data/interaction_data/reduced_parasites.csv"

# global variables:
START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)
freelivings = []
parasites = []
current_freelivings = []
current_parasites = []
nr_leave_nodes = 0
nr_used_freelivings = 0
nr_used_parasites = 0
unknown = 0
nodelist = []

def main():
    global START_TIME
    global CURRENT_TIME
    global freelivings
    global parasites
    global current_freelivings
    global current_parasites
    global nr_leave_nodes
    global nr_used_freelivings
    global nr_used_parasites
    global unknown
    global nodelist

    subtree_names = ['Eukaryota', 'Metazoa', 'Chloroplastida', 'Fungi', 'Vertebrata', 'Tetrapoda', 
        'Nematoda', 'Mammalia', 'Primates', 'Hominidae']

    print(colored("------------------------ build nodelists ------------------------", "green"))
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    CURRENT_TIME = print_time(START_TIME)

    print(colored("---------------- read parasites and freelivings ----------------", "green"))
    print("Freelivings:")
    freelivings = read_tags(path_freelivings)
    print("Parasites:")
    parasites = read_tags(path_parasites)
    CURRENT_TIME = print_time(CURRENT_TIME)

    for item in subtree_names:
        print(colored("---------------- read tree ----------------", "green"))
        subtree_path = '../data/subtree/' + item + '.tre'
        print("Build nodelist for:", item)
        tree = Phylo.read(subtree_path, 'newick')
        print(colored("---------------- tag tree ----------------", "green"))
        current_freelivings = deepcopy(freelivings)
        current_parasites = deepcopy(parasites)
        fill_tree_with_tags(tree.clade, item)
        print(colored(nr_leave_nodes, 'blue'), "leave nodes are in the tree")
        print(colored(nr_used_freelivings, 'blue'), "freeliving tags were used,", colored(nr_used_parasites, 'blue'), "parasite tags were used =>", colored(unknown, 'blue'), "unknown leave nodes")
        print("Rootnode, Depths: [Min, Max, Mean], Originaltag, Finaltag, Nr_children")
        print(nodelist[0])
        # ---- reset countings ----
        nr_leave_nodes = 0
        nr_used_freelivings = 0
        nr_used_parasites = 0
        unknown = 0
        nodelist = []
        CURRENT_TIME = print_time(CURRENT_TIME)
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
                tag_array.append("ott" + id_array[1])
        print('number of tag:', nr_tags)
    return tag_array

def fill_tree_with_tags(subtree, subtree_name):
    global current_freelivings
    global current_parasites
    global nr_leave_nodes
    global nr_used_freelivings
    global nr_used_parasites
    global unknown
    global nodelist
    
    ott = subtree.name.split("$")[0] # remove index
    depths = [1, 1, 1]
    #              0    1       2           3           4
    # nodelist - [id, depths, nr_children, originaltag, finaltag]
    nodelist.append([ott, depths, len(subtree.clades), "", ""])
    current_list_index = len(nodelist) - 1

    if subtree.is_terminal():
        tag_boolf = get_tag(ott, current_freelivings)
        tag_boolp = get_tag(ott, current_parasites)
        current_freelivings = tag_boolf[1]
        current_parasites = tag_boolp[1] 
        nr_leave_nodes += 1
        if tag_boolp[0]:
            nr_used_parasites += 1
            nodelist[current_list_index][3] = "2"
        else:
            if tag_boolf[0]:
                nodelist[current_list_index][3] = "1"
                nr_used_freelivings += 1
            else:
                nodelist[current_list_index][3] = "NA"
                unknown += 1
    else:
        min_depth = float('inf')
        max_depth = 0
        mean_depth = 0
        child_depth = 0
        for clade in subtree.clades:
            result = fill_tree_with_tags(clade, subtree_name)
            depths = result[0]
            current_freelivings = result[1]
            current_parasites = result[2]
            if depths[0] < min_depth:
                min_depth = depths[0]
            if depths[1] > max_depth:
                max_depth = depths[1]
            child_depth = child_depth + depths[2]
        mean_depth = child_depth/len(subtree.clades) + 1
        depths = [min_depth + 1, max_depth + 1, mean_depth]
        nodelist[current_list_index][1] = depths
    # -------------------------------------------------
    csv_title = '../data/nodelist/' + subtree_name + '.csv' 
    nodelist_file = open(csv_title, 'a')
    writer = csv.writer(nodelist_file)
    writer.writerow((nodelist[current_list_index])) 
    nodelist_file.close()
    # -------------------------------------------------
    return [depths, current_freelivings, current_parasites]

def get_tag(name, species_list):
    # Checks for the presence of name in any string in the list
    for item in species_list:
        # print(item, '==?', name)
        # ott_item = 'ott' + item
        mrcaott_item = 'mrca' + item + 'ott'
        if item == name or name.endswith(item) or name.startswith(mrcaott_item):
            print(item, '==', name)
            species_list.remove(item)
            return [True, species_list]
        if not (name.startswith('mrca') or name.startswith('ott')):
            print(name)
    return [False, species_list]

main()
