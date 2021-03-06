"""This module builds a random binary tree and give tags to every node."""

import numpy as np
from Bio import Phylo

# global variables / parameters:
A_FL = 8.0
B_FL = 3.0
A_P = 3.0
B_P = 8.0
ROOTNODEVALUE = 1

def get_random_tagged_tree(number_leafnodes, lower, upper):
    """build a random binary tree fully tagged with FL and P"""
    percentage_parasites = 0
    current_tree = None
    boolean = True
    while boolean:
        # randomized(cls, taxa, branch_length=1.0, branch_stdev=None) 
        #   Create a randomized bifurcating tree given a list of taxa.
        #   https://github.com/biopython/biopython/blob/master/Bio/Phylo/BaseTree.py
        current_tree = Phylo.BaseTree.Tree.randomized(number_leafnodes)
        result = tag_tree(current_tree.clade, [], ROOTNODEVALUE, [0, 0])
        nodelist = result[0]
        leaf_distr = result[1]
        percentage_parasites = leaf_distr[1] / (leaf_distr[0] + leaf_distr[1]) * 100
        # 40% parasites?
        if lower < percentage_parasites < upper:
            boolean = False
    print(percentage_parasites, '% parasites,', 100 - percentage_parasites, '% free-living')
    return [current_tree, nodelist]

def tag_tree(subtree, nodelist, random_number, leaf_dist):
    """Function tags all nodes of a given (binary) subtree with names FL or P."""
    # Arguments:
    #   subtree
    #   nodelist      - [id, originaltag, finaltag, calc[taglist]]
    #   random_number - in [0, 1]
    #   leaf_dist     - [#FL, #P] - distribution...
    if not subtree.name:
        subtree.name = '0'  # rootnode
    if random_number >= 0.5:
        # subtree.confidence = 1
        nodelist.append([subtree.name, 'FL', '', []])
    else:
        # subtree.confidence = 0
        nodelist.append([subtree.name, 'P', '', []])
    if subtree.is_terminal():
        nodelist[-1][3].append(nodelist[-1][1])
        if nodelist[-1][1] == 'FL':
            leaf_dist[0] = leaf_dist[0] + 1
        else:
            leaf_dist[1] = leaf_dist[1] + 1
    else:
        for clade in subtree.clades:
            if random_number >= 0.5:
                # freeliving_distribution:
                new_random = np.random.beta(a=A_FL, b=B_FL)
            else:
                # parasite_distribution:
                new_random = np.random.beta(a=A_P, b=B_P)
            result = tag_tree(clade, nodelist, new_random, leaf_dist)
            nodelist = result[0]
            leaf_dist = result[1]
    return [nodelist, leaf_dist]
