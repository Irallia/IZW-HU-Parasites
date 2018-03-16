"""Maximum parsimony algorithm from Sankoff implemented in the R package castor"""

import rpy2.robjects
from Bio import Phylo

from code.utilities.Helpers import find_element_in_nodelist
from random import randint

def sankoff_parsimony(tree, nodelist):
    """Using rpy2 for forwarding to R code"""

    # ---- cache tree for R script ---
    random_name = str(randint(0, 1000))
    path_simulated_tree = 'code/bufferfiles/simulated_tree' + random_name + '.tre'
    path_tagged_tree = 'code/bufferfiles/tagged_tree' + random_name + '.tre'

    Phylo.write(tree, path_simulated_tree , 'newick')
    prepare_tree(tree.clade, nodelist)
    Phylo.write(tree, path_tagged_tree, 'newick')
    
    # -------- R code --------
    
    path = "code/utilities/castor_parsimony_simulation.R"
    f = open(path, "r")
    code = ''.join(f.readlines())
    print("---------------- prepare R script ----------------")
    code_Array = code.split("data/subtree/Eukaryota.tre")
    code = path_simulated_tree.join(code_Array)
    code_Array = code.split("code/bufferfiles/tagged_tree.tre")
    code = path_tagged_tree.join(code_Array)

    result = rpy2.robjects.r(code)
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

def prepare_tree(subtree, nodelist):
    """tag all leafs"""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    if subtree.is_terminal():
        element = find_element_in_nodelist(subtree.name, nodelist)
        if len(element[4][0]) > 1:
            subtree.name = ''
        else:
            subtree.name = str(element[4][0][0])
    for clade in subtree.clades:
        prepare_tree(clade, nodelist)
    return
