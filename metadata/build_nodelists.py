import csv
import datetime
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored

from Helpers import print_time

path_parasites = "../data/interaction_data/parasite.csv"
path_freelivings = "../data/interaction_data/freeliving.csv"

# global variables:
START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)

def main():
    global START_TIME
    global CURRENT_TIME

    subtree_names = ['Eukaryota', 'Fungi', 'Metazoa', 'Nematoda', 'Vertebrata', 
        'Tetrapoda', 'Mammalia', 'Primates', 'Hominidae', 'Chloroplastida']

    print(colored("------------------------ start tree calculation ------------------------", "green"))
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    CURRENT_TIME = print_time(START_TIME)

    for item in subtree_names:
        print(colored("---------------- read tree ----------------", "green"))
        subtree_path = '../data/subtree/' + item + '.tre'
        print("Build nodelist for:", item)
        tree = Phylo.read(subtree_path, 'newick')
        CURRENT_TIME = print_time(CURRENT_TIME)
        print(colored("---------------- tag tree ----------------", "green"))
        fill_tree_with_tags(tree.clade, item)
        CURRENT_TIME = print_time(CURRENT_TIME)
        print(colored("--------------------------------", "green"))
    return

def fill_tree_with_tags(subtree, subtree_name):
    nodelist = []
    #              0    1       2           3           4
    # nodelist - [id, depth, originaltag, finaltag, nr_children

    depths = [1, 1, 1]
    nodelist.append([subtree.name, depths, "", "", len(subtree.clades)])
    current_list_index = len(nodelist) - 1

    if not subtree.is_terminal():
        min_depth = float('inf')
        max_depth = 0
        mean_depth = 0
        child_depth = 0

        for clade in subtree.clades:
            depths = fill_tree_with_tags(clade, subtree_name)
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
    fp = open(csv_title, 'a')
    writer = csv.writer(fp)
    writer.writerow((nodelist[current_list_index])) 
    fp.close()
    # -------------------------------------------------
    return depths

main()
