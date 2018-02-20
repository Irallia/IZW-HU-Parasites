import ast
import csv
import datetime
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored

from Helpers import find_element_in_nodelist, print_time

# global variables:
START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)
nodelist = []

def main():
    global START_TIME
    global CURRENT_TIME
    global nodelist
    
    print(colored("---------------- read tree ----------------", "green"))
    subtree_path = '../data/subtree/Eukaryota.tre'
    tree = Phylo.read(subtree_path, 'newick')
    CURRENT_TIME = print_time(CURRENT_TIME)

    print(colored("---------------- read nodelist ----------------", "green"))
    nodelist_path = '../results/Eukaryota-taxa.csv' 
    #               0       1   2       3           4       5           6           7
    # nodelist - [ott_id, name, rank, uniqname, depths, nr_children, originaltag, finaltag]
    with open(nodelist_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if row != []:
                ott_id = row[0]
                originaltag = row[6]
                finaltag = row[7]
                print(ott_id, originaltag, finaltag)
                nodelist.append([ott_id, originaltag, finaltag])
    CURRENT_TIME = print_time(CURRENT_TIME)

    print(colored("---------------- prepare tree ----------------", "green"))
    prepare_tree(tree.clade)
    print(colored("---------------- Save tree ----------------", "green"))
    Phylo.write(tree, 'results/Eukaryota_tree.tre', 'newick')
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
    if element[0].split("$")[1] != subtree.name:
        print(subtree.name)
        print(element)
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
