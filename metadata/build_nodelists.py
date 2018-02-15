import csv
import datetime
from copy import deepcopy
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored, cprint

from Helpers import print_time

# path_freelivings = "../data/interaction_data/reduced_freelivings.csv"
# path_parasites = "../data/interaction_data/reduced_parasites.csv"
path_freelivings = "../data/interaction_data/freelivings.csv"
path_parasites = "../data/interaction_data/parasites.csv"

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
doubleTagged = 0
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
    global doubleTagged

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
    current_freelivings = deepcopy(freelivings)
    current_parasites = deepcopy(parasites)
    fill_tree_with_tags(tree.clade, 0)
    print(colored(nr_leave_nodes, 'blue'), "leave nodes are in the tree")
    print(colored(nr_used_freelivings, 'blue'), "freeliving tags were used,", colored(nr_used_parasites, 'blue'), "parasite tags were used =>", colored(unknown, 'blue'), "unknown leave nodes")
    print("Rootnode, Depth, Heigths: [Min, Max, Mean], Originaltag, Finaltag, Nr_children")
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

def fill_tree_with_tags(subtree, depth):
    global nr_leave_nodes
    global nr_used_freelivings
    global nr_used_parasites
    global unknown
    global nodelist
    global doubleTagged
    
    ott = subtree.name.split("$")[0] # remove index
    heights = [1, 1, 1]
    #              0    1       2           3           4           5
    # nodelist - [id, depth, heights, nr_children, originaltag, finaltag]
    nodelist.append([ott, depth, heights, len(subtree.clades), "", ""])
    current_list_index = len(nodelist) - 1

    if subtree.is_terminal():
        nr_leave_nodes += 1
        tag_boolp = get_tag(ott, 'P')
        if tag_boolp:
            nr_used_parasites += 1
            nodelist[current_list_index][4] = "2"
            if (get_tag(ott, 'FL')):
                doubleTagged += 1
        else:
            tag_boolf = get_tag(ott, 'FL')
            if tag_boolf:
                nr_used_freelivings += 1
                nodelist[current_list_index][4] = "1"
            else:
                nodelist[current_list_index][4] = "NA"
                unknown += 1
    else:
        min_heigth = float('inf')
        max_heigth = 0
        mean_heigth = 0
        child_heigth = 0
        for clade in subtree.clades:
            heights = fill_tree_with_tags(clade, depth + 1)
            if heights[0] < min_heigth:
                min_heigth = heights[0]
            if heights[1] > max_heigth:
                max_heigth = heights[1]
            child_heigth = child_heigth + heights[2]
        mean_heigth = child_heigth/len(subtree.clades) + 1
        heights = [min_heigth + 1, max_heigth + 1, mean_heigth]
        nodelist[current_list_index][2] = heights
    # -------------------------------------------------
    csv_title = '../data/nodelist/Eukaryota.csv' 
    nodelist_file = open(csv_title, 'a')
    writer = csv.writer(nodelist_file)
    writer.writerow((nodelist[current_list_index])) 
    nodelist_file.close()
    # -------------------------------------------------
    return heights

def get_tag(name, tag):
    global current_freelivings
    global current_parasites
    if tag == 'FL':
        species_list = current_freelivings
    else:
        species_list = current_parasites
    # Checks for the presence of name in any string in the list
    for item in species_list:
        # mrcaott_item = 'mrca' + item + 'ott'
        if item == name or name.endswith(item): # or name.startswith(mrcaott_item):
            species_list.remove(item)
            return True
    return False

main()
