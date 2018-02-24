import csv
import datetime
from code.utilities.Helpers import print_time
from code.utilities.nodelist_util import read_tags, tag_node
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored, cprint

# path_freelivings = "./data/interaction_data/reduced_freelivings.csv"
# path_parasites = "./data/interaction_data/reduced_parasites.csv"
path_freelivings = "./data/interaction_data/freelivings.csv"
path_parasites = "./data/interaction_data/parasites.csv"

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
    subtree_path = './data/subtree/Eukaryota.tre'
    print("Build nodelist for: Eukaryota")
    tree = Phylo.read(subtree_path, 'newick')
    print(colored("---------------- tag tree ----------------", "green"))
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

def fill_tree_with_tags(subtree, depth):
    global nr_leave_nodes
    global nr_used_freelivings
    global nr_used_parasites
    global unknown
    global nodelist
    global doubleTagged
    
    ott = subtree.name.split("$")[0] # remove index
    heights = [1, 1, 1]
    
    #                   0    1              2       3       4           5
    # nodelist      - [id, originaltag, finaltag, depth, heights, nr_children]
    nodelist.append([ott, "", "", depth, heights, len(subtree.clades)])
    current_list_index = len(nodelist) - 1

    if subtree.is_terminal():
        stats = [nr_leave_nodes, nr_used_parasites, nr_used_freelivings, unknown, doubleTagged]
        stats = tag_node(nodelist, current_list_index, ott, [freelivings, parasites], stats)
        nr_leave_nodes = stats[0]
        nr_used_parasites = stats[1]
        nr_used_freelivings = stats[2]
        unknown = stats[3]
        doubleTagged = stats[4]
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
        nodelist[current_list_index][4] = heights
    # -------------------------------------------------
    csv_title = './data/nodelist/Eukaryota.csv' 
    nodelist_file = open(csv_title, 'a')
    writer = csv.writer(nodelist_file)
    writer.writerow((nodelist[current_list_index])) 
    nodelist_file.close()
    # -------------------------------------------------
    return heights

main()
