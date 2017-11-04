"""This module builds a random binary tree and give tags to every node."""

import numpy as np
from Bio import Phylo

import Helpers

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
        leaf_distrr = result[1]
        percentage_parasites = leaf_distrr[1] / (leaf_distrr[0] + leaf_distrr[1]) * 100
        # 40% parasites?
        if lower < percentage_parasites < upper:
            boolean = False
    print(percentage_parasites, '% parasites,', 100 - percentage_parasites, '% free-living')
    return [current_tree, nodelist]

def tag_tree(subtree, nodelist, random_number, leaf_distr):
    """Function tags all nodes of a given (binary) subtree with names FL or P."""
    # Arguments:
    #   subtree
    #   nodelist      - [id, depth, originaltag, finaltag, calc[taglist]]
    #   random_number - in [0, 1]
    #   leaf_distr     - [#FL, #P] - distribution...
    if not subtree.name:
        subtree.name = '0'  # rootnode
    if random_number >= 0.5:
        originaltag = 'FL'
    else:
        originaltag = 'P'
    if subtree.is_terminal():
        depth = 1
        nodelist.append([subtree.name, depth, originaltag, '', []])
        nodelist[-1][4].append(nodelist[-1][2]) # if leaf node, than set finaltag
        if nodelist[-1][1] == 'FL':
            leaf_distr[0] = leaf_distr[0] + 1
        else:
            leaf_distr[1] = leaf_distr[1] + 1
    else:
        for clade in subtree.clades:
            if random_number >= 0.5:
                # freeliving_distribution:
                new_random = np.random.beta(a=A_FL, b=B_FL)
            else:
                # parasite_distribution:
                new_random = np.random.beta(a=A_P, b=B_P)
            # TODO::!!!
            result = tag_tree(clade, nodelist, new_random, leaf_distr)
            nodelist = result[0]
            leaf_distr = result[1]
        left_child = Helpers.find_element_in_nodelist(subtree.clades[0].name, nodelist)
        right_child = Helpers.find_element_in_nodelist(subtree.clades[1].name, nodelist)
        print(left_child)
        depth = (left_child[1] + right_child[1])/2 + 1 
        nodelist.append([subtree.name, depth, originaltag, '', []])
    return [nodelist, leaf_distr]

def get_non_binary_tree(subtree, nodelist):
    for clade in subtree.clades:
        if not clade.is_terminal():
            # print('-- go deeper --')
            get_non_binary_tree(clade, nodelist)
    i = 0
    while i != len(subtree.clades):
        if subtree.clades[i].is_terminal():
            i += 1
        else:
            element = Helpers.find_element_in_nodelist(subtree.clades[i].name, nodelist)
            limit = get_limit(element[1])
            print('i=', i)
            new_random = np.random.uniform(0,1) # choose if we want to delete ourselve
            print(new_random, ' < ', limit)
            if new_random < limit: # or new_random < 0.9:
                print('delete me!')
                subtree.clades += subtree.clades[i].clades # add children
                del subtree.clades[i]   # delete internal node
            else:
                i += 1
    return


def get_limit(depth):
    limit = 1/(depth/4)
    if limit < 0.1:
        limit = 0.1
    print('depth=', depth, ' -> limit=', str(round(limit,3)))
    return limit
