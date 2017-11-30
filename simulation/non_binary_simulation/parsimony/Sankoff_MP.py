"""Maximum parsimony algorithm from Sankoff implemented in the R package castor"""

import rpy2.robjects
from Bio import Phylo

from utilities import Helpers

def sankoff_parsimony(tree, nodelist):
    """Using rpy2 for forwarding to R code"""
    newick_tree = "(((parasite,freeliving,parasite),(freeliving,freeliving)),freeliving);"

    # ---- cache tree for R script ---
    prepare_tree(tree.clade, nodelist)

    Phylo.write(tree, 'bufferfiles/simulated_tree.tre', 'newick')

    # -------- R code --------
    
    path = "utilities/castor_parsimony_simulation.R"
    f = open(path, "r")
    code = ''.join(f.readlines())
    result = rpy2.robjects.r(code)
    # assume that...
    likelihoods = rpy2.robjects.globalenv['likelihoods']
    print(likelihoods)
    return

def prepare_tree(subtree, nodelist):
    """tag all leafs"""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    if subtree.is_terminal():
        element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
        originaltag = element[2]
        if originaltag == 'P':
            subtree.name = "1"
        else:
            subtree.name = "2"
    # else:
    #     subtree.name = ''
    for clade in subtree.clades:
        prepare_tree(clade, nodelist)
    return
