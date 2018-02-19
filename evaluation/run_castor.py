"""Maximum parsimony algorithm from Sankoff implemented in the R package castor"""

import ast
import csv
import datetime
import sys
from time import gmtime, strftime

import rpy2.robjects
from Bio import Phylo
from termcolor import colored

from Helpers import find_element_in_nodelist, print_time

# values for simulation:
index = sys.argv[1]
border = int(sys.argv[2])

# global variables:
START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)
r_path = "../simulation/utilities/castor_parsimony_simulation.R"
nodelist = []

print(colored("------------------------ Sankoff Maximum Parsimony ------------------------", "green"))

def main():
    global START_TIME
    global CURRENT_TIME
    global nodelist
    global index
    global border

    print('Run castor - Sankoff parsimony - for Eukaryota')
    print(colored("---------------- read tree ----------------", "green"))
    subtree_path = '../data/subtree/Eukaryota.tre'
    tree = Phylo.read(subtree_path, 'newick')
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- read nodelist ----------------", "green"))
    nodelist_path = '../data/evaluation/Eukaryota'+ index + '-' + str(border) +'.csv'
    #              0        1           2
    # nodelist - [id, originaltag, finaltag]
    with open(nodelist_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if row != []:
                ott = row[0]
                originaltag = row[1]
                finaltag = row[2]
                nodelist.append([ott, originaltag, finaltag])
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- Sankoff parsimony ----------------", "green"))
    sankoff_parsimony(tree)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- Save nodelist ----------------", "green"))
    nodelist_path = '../data/evaluation/Eukaryota'+ index + '-' + str(border) +'-castor.csv'
    header = ['ott_id', 'originaltag', 'finaltag']
    with open(nodelist_path, 'w') as nodelist_file:
        writer = csv.writer(nodelist_file, delimiter=',')
        writer.writerow(header)
        for row in nodelist:
            writer.writerow(row)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("--------------------------------", "green"))
    return

def sankoff_parsimony(tree):
    """Using rpy2 for forwarding to R code"""
    # Arguments:
    #   subtree
    #              0        1           2
    #   nodelist - [id, originaltag, finaltag]
    global nodelist

    # ---- cache tree for R script ---

    Phylo.write(tree, 'bufferfiles/simulated_tree.tre', 'newick')

    prepare_tree(tree.clade)
    Phylo.write(tree, 'bufferfiles/simulated_tagged_tree.tre', 'newick')
    
    # -------- R code --------
    
    f = open(r_path, "r")
    code = ''.join(f.readlines())
    rpy2.robjects.r(code)
    # assume that...
    likelihoods = rpy2.robjects.globalenv['likelihoods'][0]
    # The rows in this matrix will be in the order in which tips and
    # nodes are indexed in the tree, i.e. the rows 1,..,Ntips store the probabilities for
    # tips, while rows (Ntips+1),..,(Ntips+Nnodes) store the probabilities for nodes.
    leaf_nodes = rpy2.robjects.globalenv['state_ids']
    number_of_tips = rpy2.robjects.globalenv['number_of_tips']
    internal_nodes = rpy2.robjects.globalenv['internal_nodes']

    l = int(len(likelihoods)/3)
        
    j = 0
    k = 0
    for i in range(2*l, 3*l):
        if j < number_of_tips[0]:
            element = find_element_in_nodelist(leaf_nodes[j], nodelist)
            if element[3] == '':    # if unknown
                # set finaltag:
                element[3] = likelihoods[i]
            j += 1
        else:
            element = find_element_in_nodelist(internal_nodes[k], nodelist)
            # set finaltag:
            element[3] = likelihoods[i]
            k += 1
    return

def prepare_tree(subtree):
    """tag all leafs"""
    # Arguments:
    #   subtree
    #              0        1           2
    #   nodelist - [id, originaltag, finaltag]
    if subtree.is_terminal():
        element = find_element_in_nodelist(subtree.name, nodelist)
        if element[2] == 'NA':
            subtree.name = ''
        else:
            subtree.name = str(element[2])
    for clade in subtree.clades:
        prepare_tree(clade)
    return

main()
