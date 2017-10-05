import random
import pylab

# StringIO no longer exists in 3.x. Use either io.StringIO for text or io.BytesIO for bytes.
# from cStringIO import StringIO
from io import StringIO
from Bio import Phylo

# global variables / parameters:
VARIANCE = 0.2
ROOTNODEVALUE = 0.7

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
        current_tree.name = 'random tree'
        # Phylo.draw(current_tree)
        leaf_distr = tag_tree(current_tree.clade, ROOTNODEVALUE, [0, 0])
        current_tree.name = 'tagged tree'
        percentage_parasites = leaf_distr[1] / (leaf_distr[0] + leaf_distr[1]) * 100
        # 40% parasites?
        if lower < percentage_parasites < upper:
            boolean = False
    print(percentage_parasites, '% parasites,', 100 - percentage_parasites, '% free-living')
    return current_tree

def tag_tree(subtree, random_number, leaf_dist):
    """Function tags all nodes of a given (binary) subtree with names FL or P."""
    # Arguments:
    #   subtree
    #   random_number - in [0, 1]
    #   leaf_dist     - [#FL, #P]
    id = '0'
    if subtree.name:
        id = subtree.name
    if random_number >= 0.5:
        subtree.name = id + '-FL'
    else:
        subtree.name = id + '-P'
    if subtree.is_terminal():
        if subtree.name.split('-')[1] == 'FL':
            leaf_dist[0] = leaf_dist[0] + 1
        else:
            leaf_dist[1] = leaf_dist[1] + 1
    else:
        for clade in subtree.clades:
            # random.gauss(mu, sigma) -> Gaussian distribution, mu: mean, sigma: standard deviation.
            new_random = min(1, max(0, random.gauss(random_number, VARIANCE)))
            leaf_dist = tag_tree(clade, new_random, leaf_dist)
    return leaf_dist

def untag_tree(subtree):
    """Function untags all internal nodes."""
    # Arguments:
    #   subtree
    if not subtree.is_terminal():
        subtree.name = subtree.name.split('-')[0]
        for clade in subtree.clades:
            untag_tree(clade)
    return
