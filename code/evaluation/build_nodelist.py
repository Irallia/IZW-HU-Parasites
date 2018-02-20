import csv
import datetime
from code.utilities.Helpers import print_time
from code.utilities.nodelist_util import read_tags, tag_node
from copy import deepcopy
from random import shuffle, uniform
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored, cprint

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

index = -1
border = -1

def build_nodelist(ind, bord):
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

    index = ind
    border = bord

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
    # delete 100 random lines ..
    i = 0
    while i < border:
        rand = uniform(0, 1)
        if rand < 0.5:
            freelivings.pop()
        elif rand > 0.5:
            parasites.pop()
        else:
            i -=1
        i += 1

    fill_tree_with_tags(tree.clade)
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

def fill_tree_with_tags(subtree):
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
        stats = [nr_leave_nodes, nr_used_parasites, nr_used_freelivings, unknown, doubleTagged]
        tag_node(nodelist, current_list_index, ott, [freelivings, parasites], stats)
    else:
        for clade in subtree.clades:
            fill_tree_with_tags(clade)
    # -------------------------------------------------
    csv_title = '../data/evaluation/Eukaryota'+ index + '-' + str(border) +'.csv' 
    nodelist_file = open(csv_title, 'a')
    writer = csv.writer(nodelist_file)
    writer.writerow((nodelist[current_list_index])) 
    nodelist_file.close()
    # -------------------------------------------------
    return
