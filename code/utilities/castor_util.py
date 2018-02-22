from code.utilities.Helpers import find_element_in_nodelist

import rpy2.robjects
from Bio import Phylo

r_path = "./code/utilities/castor_parsimony_simulation.R"
nodelist = []


def sankoff_parsimony(tree, current_nodelist):
    """Using rpy2 for forwarding to R code"""
    # Arguments:
    #   tree
    #                   0    1              2       3       4           5
    #   nodelist    - [id, originaltag, finaltag, depth, heights, nr_children]
    global nodelist
    nodelist = current_nodelist

    # ---- cache tree for R script ---

    Phylo.write(tree, './code/bufferfiles/simulated_tree.tre', 'newick')

    prepare_tree(tree.clade)
    Phylo.write(tree, './code/bufferfiles/simulated_tagged_tree.tre', 'newick')
    
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
            if element[2] == '':    # if unknown
                # set finaltag:
                element[2] = likelihoods[i]
            j += 1
        else:
            element = find_element_in_nodelist(internal_nodes[k], nodelist)
            # set finaltag:
            element[2] = likelihoods[i]
            k += 1
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
