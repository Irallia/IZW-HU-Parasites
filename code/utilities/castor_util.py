import ast
import csv
import random
from code.utilities.Helpers import find_element_in_nodelist

import rpy2.robjects
from Bio import Phylo
from termcolor import colored

r_path = "./code/utilities/castor_parsimony_simulation.R"
nodelist = []


def sankoff_parsimony(run_id):
    """Using rpy2 for forwarding to R code"""
    # Arguments:
    #   tree
    #                   0    1              2       3       4           5
    #   nodelist    - [id, originaltag, finaltag, depth, heights, nr_children]
    #   run_id
    global nodelist

    read_nodelist()

    tagged_tree_path = 'code/bufferfiles/simulated_tagged_tree.tre'
    if run_id >= 0:
        randomly_change_nodelist()
        tagged_tree_path = './code/bufferfiles/simulated_tagged_tree' + str(run_id) + '.tre'

    # ---- cache tree for R script ---
    cache_tree(tagged_tree_path)
    
    # -------- R code --------
    
    f = open(r_path, "r")
    code = ''.join(f.readlines())
    if run_id >= 0:
        print(colored("---------------- run castor ----------------", "green"))
        code_Array = code.split("code/bufferfiles/simulated_tagged_tree.tre")
        code = tagged_tree_path.join(code_Array)

    print(colored("---------------- prepare R script ----------------", "green"))

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
            if element[2] == '':    # if unknown
                # set finaltag:
                element[2] = likelihoods[i]
            j += 1
        else:
            element = find_element_in_nodelist(internal_nodes[k], nodelist)
            # set finaltag:
            element[2] = likelihoods[i]
            k += 1
    return nodelist

def read_nodelist():
    global nodelist

    print(colored("---------------- read nodelist ----------------", "green"))
    nodelist_path = './data/nodelist/Eukaryota.csv' 
    #                0    1              2       3       4           5
    # nodelist    - [id, originaltag, finaltag, depth, heights, nr_children]
    nodelist = []
    with open(nodelist_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if row != []:
                ott = row[0]
                originaltag = row[1]
                finaltag = row[2]
                depth = int(row[3])
                heights = ast.literal_eval(row[4])
                nr_children = int(row[5])
                nodelist.append([ott, originaltag, finaltag, depth, heights, nr_children])
    return

def randomly_change_nodelist():
    print(colored("---------------- randomly change nodelist ----------------", "green"))
    #                   0    1              2       3       4           5
    # nodelist      - [id, originaltag, finaltag, depth, heights, nr_children]
    global nodelist
    border = 100
    changed = 0
    while changed < border:
        index = random.randrange(len(nodelist))
        element = nodelist[index]
        if element[1] != 'NA':
            element[1] = 'NA'
            nodelist[index] = element
            changed +=1
    return

def cache_tree(tagged_tree_path):
    print(colored("---------------- read tree ----------------", "green"))
    tree_path = './data/subtree/Eukaryota.tre'
    tree = Phylo.read(tree_path, 'newick')

    prepare_tree(tree.clade)
    Phylo.write(tree, tagged_tree_path, 'newick')
    return

def prepare_tree(subtree):
    """tag all leafs"""
    # Arguments:
    #   subtree
    #                   0    1              2       3       4           5
    # nodelist      - [id, originaltag, finaltag, depth, heights, nr_children]
    global nodelist

    if subtree.is_terminal():
        element = find_element_in_nodelist(subtree.name, nodelist)
        if element[1] == 'NA':
            subtree.name = ''
        else:
            subtree.name = str(element[1])
    for clade in subtree.clades:
        prepare_tree(clade)
    return
