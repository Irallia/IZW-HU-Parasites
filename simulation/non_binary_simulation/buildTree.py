"""This module builds a random binary tree and give tags to every node."""

from copy import deepcopy

from Bio import Phylo
from numpy import random

from utilities import Helpers

# global variables / parameters:
#   for freeliving_distribution
A_FL = 8.0
B_FL = 3.0
#   for parasite_distribution
A_P = 3.0
B_P = 8.0

def get_random_tagged_tree(number_leafnodes, percentage):
    """build a random binary tree fully tagged with FL and P"""
    percentage_parasites = 0
    # randomized(cls, taxa, branch_length=1.0, branch_stdev=None) 
    #   Create a randomized bifurcating tree given a list of taxa.
    #   https://github.com/biopython/biopython/blob/master/Bio/Phylo/BaseTree.py
    randomized_tree = Phylo.BaseTree.Tree.randomized(number_leafnodes)
    randomized_tree.clade.name = 'root'
    current_tree = deepcopy(randomized_tree)
    boolean = True
    print("---- tag tree ----")
    while boolean:
        result = tag_tree(current_tree.clade, [], 'FL', [0, 0])
        nodelist = result[0]
        leaf_distr = result[1]
        # %P = #FL / (#P + #FL) * 100
        percentage_parasites = leaf_distr[1] / (leaf_distr[0] + leaf_distr[1]) * 100
        print("tried", percentage_parasites, "% of parasites")  # 40% parasites?
        if (percentage - 5) < percentage_parasites < (percentage + 5):
            boolean = False
        current_tree = deepcopy(randomized_tree)
    print("----")
    print(percentage_parasites, '% parasites,', 100 - percentage_parasites, '% free-living')
    return [current_tree, nodelist]

def tag_tree(subtree, nodelist, father_tag, leaf_distr):
    """Function tags all nodes of a given (binary) subtree with names FL or P."""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    #   father_tag  - FL or P
    #   leaf_distr  - [#FL, #P] - distribution of FL and P in the leave nodes
    depth = -1
    if father_tag == 'FL':
        # freeliving_distribution:
        new_random = random.beta(a=A_FL, b=B_FL)
    else:
        # parasite_distribution:
        new_random = random.beta(a=A_P, b=B_P)

    tag = 'FL'
    if new_random < 0.5:
        tag = 'P'
    #               [id, depth, originaltag, finaltag, calc[taglist]]
    nodelist.append([subtree.name, depth, tag, '', []])
    current_list_index = len(nodelist) - 1
    # if leaf node, then depth = 1, set finaltag, increase leaf distribution
    if subtree.is_terminal():
        depth = 1
        nodelist[current_list_index][3] = tag
        nodelist[current_list_index][4].append([tag])
        if tag == 'FL':
            leaf_distr[0] = leaf_distr[0] + 1
        else:
            leaf_distr[1] = leaf_distr[1] + 1
    else:
        child_depth = 0
        for clade in subtree.clades:
            result = tag_tree(clade, nodelist, tag, leaf_distr)
            nodelist = result[0]
            leaf_distr = result[1]
            child_depth = child_depth + result[2]
        depth = child_depth/len(subtree.clades) + 1 
    nodelist[current_list_index][1] = depth
    return [nodelist, leaf_distr, depth]

def get_non_binary_tree(subtree, nodelist):
    i = 0
    while i != len(subtree.clades):
        if subtree.clades[i].is_terminal():
            i += 1
        else:
            element = Helpers.find_element_in_nodelist(subtree.clades[i].name, nodelist)
            limit = get_limit(element[1])
            # print('i=', i, 'len=', len(subtree.clades))
            # numpy.random.uniform(low=0.0, high=1.0, size=None)
            new_random = random.uniform() # choose if we want to delete ourselve
            # print(new_random, ' < ', limit)
            if new_random < limit: # or new_random < 0.9:
                # print('delete me!')
                subtree.clades += subtree.clades[i].clades # add children
                del subtree.clades[i]   # delete internal node
                # current clades: clade_1 clade_2 ... clade_i-1 clade_i ... clade:_n
                # add children of clade_i, delete clade_i
                # new clades:clade_1 clade_2 ... clade_i-1 child_clade_1 ... child_clade_m ... clade:_n
                # child_clade_1 is new clade i
            else:
                get_non_binary_tree(subtree.clades[i], nodelist)
                i += 1
    return

def get_limit(depth):
    limit = 1 - 1/((depth+3)/4)
    if limit < 0.1:
        limit = 0.1
    # print('depth=', depth, ' -> limit=', str(round(limit,3)))
    return limit
