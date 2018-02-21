import ast
import csv
import datetime
from code.utilities.Helpers import find_element_in_nodelist, print_time
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored

# global variables:
START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)
nodelist = []

def main():
    global START_TIME
    global CURRENT_TIME
    global nodelist
    
    print(colored("---------------- read tree ----------------", "green"))
    subtree_path = './data/subtree/Eukaryota.tre'
    tree = Phylo.read(subtree_path, 'newick')
    CURRENT_TIME = print_time(CURRENT_TIME)

    print(colored("---------------- read nodelist ----------------", "green"))
    nodelist_path = './data/nodelist/Eukaryota-castor.csv' 
    #                0    1              2       3       4           5
    # nodelist    - [id, originaltag, finaltag, depth, heights, nr_children]
    with open(nodelist_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader, None)      # skip the header
        for row in reader:
            if row != []:
                ott_id = row[0]
                originaltag = row[1]
                finaltag = row[2]
                nodelist.append([ott_id, originaltag, finaltag])
    CURRENT_TIME = print_time(CURRENT_TIME)

    print(colored("---------------- prepare tree ----------------", "green"))
    prepare_tree(tree.clade)
    print(colored("---------------- Save tree ----------------", "green"))
    Phylo.write(tree, './results/Eukaryota_tree-castor.tre', 'newick')
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("--------------------------------", "green"))
    return
    
def prepare_tree(subtree):
    """tag all leafs"""
    # Arguments:
    #   subtree
    #                   0       1           2           
    #   nodelist - [ott_id, originaltag, finaltag]
    element = find_element_in_nodelist(subtree.name, nodelist)
    if subtree.is_terminal():
        if element[1] != '':
            subtree.name = subtree.name + '$' + element[1]
        else:
            subtree.name = subtree.name + '$(' + element[2] + ')'
    else:
        subtree.name = subtree.name + '$(' + element[2] + ')'
        for clade in subtree.clades:
            prepare_tree(clade)
    return

main()
