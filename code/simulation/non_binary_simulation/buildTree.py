"""This module builds a random binary tree and give tags to every node."""

import datetime
from code.utilities.Helpers import find_element_in_nodelist, print_time
from copy import deepcopy
from random import betavariate, uniform

from Bio import Phylo

# global variable:
permitted_deviation = 0.02 # 2%

def get_random_tagged_tree(number_leafnodes, percentage_parasites, percentage_unknown, beta_distribution_parameters):
    """build a random binary tree fully tagged with FL and P"""
    # Arguments:
    #   number_leafnodes                - needed for randomized function
    #   percentage_unknown              - proportion of unknown leafnodes
    #   percentage_parasites
    #   beta_distribution_parameters    - [A_FL, B_FL, A_P, B_P]

    START_TIME = datetime.datetime.now().replace(microsecond=0)
    CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)
    print("---- randomized tree ----")
    current_percentage_parasites = 0
    # randomized(cls, taxa, branch_length=1.0, branch_stdev=None) 
    #   Create a randomized bifurcating tree given a list of taxa.
    #   https://github.com/biopython/biopython/blob/master/Bio/Phylo/BaseTree.py
    randomized_tree = Phylo.BaseTree.Tree.randomized(number_leafnodes)
    randomized_tree.clade.name = 'root'
    boolean = True
    CURRENT_TIME = print_time(START_TIME)
    print("---- tag tree ----")
    while boolean:
        current_tree = deepcopy(randomized_tree)
        result = tag_tree(current_tree.clade, [], 0, [0, 0], percentage_parasites, percentage_unknown, beta_distribution_parameters) # father_tag = 0 -> free living
        nodelist = result[1]
        leaf_distr = result[2]
        # child_depth = child_depth + result[3]
        # %P = #FL / (#P + #FL) * 100
        current_percentage_parasites = leaf_distr[1] / (leaf_distr[0] + leaf_distr[1]) 
        print("tried", current_percentage_parasites*100, "% of parasites")  # 40% parasites?
        if (percentage_parasites - permitted_deviation) < current_percentage_parasites < (percentage_parasites + permitted_deviation):
            boolean = False
    print("----")
    CURRENT_TIME = print_time(CURRENT_TIME)
    print("----")
    # print(current_percentage_parasites, '% parasites,', 100 - current_percentage_parasites, '% free-living')
    return [current_tree, nodelist]

def tag_tree(subtree, nodelist, father_tag, leaf_distr, percentage_parasites, percentage_unknown, beta_distribution_parameters):
    """Function tags all nodes of a given (binary) subtree with names FL or P."""
    # Arguments:
    #   subtree
    #                                       0   1       2           3           4
    #   nodelist                        - [id, depth, originaltag, finaltag, calc[taglist]]
    #   father_tag                      - 0 or 1 (FL or P)
    #   leaf_distr                      - [#FL, #P] - distribution of FL and P in the leave nodes
    #   percentage_unknown              - proportion of unknown leafnodes
    #   percentage_parasites
    #   beta_distribution_parameters    - [A_FL, B_FL, A_P, B_P]

    # beta distribution parameters:
    #   for freeliving_distribution
    A_FL = beta_distribution_parameters[0]
    B_FL = beta_distribution_parameters[1]
    #   for parasite_distribution
    A_P = beta_distribution_parameters[2]
    B_P = beta_distribution_parameters[3]

    depths = [1, 1, 1]
    if father_tag == 0:
        # freeliving_distribution:
        new_random = betavariate(A_FL, B_FL)
    else:
        # parasite_distribution:
        new_random = betavariate(A_P, B_P)

    tag = 0         # -> FL
    if new_random < percentage_parasites:
        tag = 1     # -> P
    #               [id, depths, originaltag, finaltag, calc[taglist]]
    nodelist.append([subtree.name, depths, tag, '', []])
    # For the quicker finding of the element in the nodelist of the accociated node.
    subtree.name = subtree.name + "$" + str(len(nodelist) - 1)
    current_list_index = len(nodelist) - 1
    if subtree.is_terminal():
        uniform_random = uniform(0, 1) # choose if we want to delete ourselve
        # unknown node?
        if (tag == 1) and (uniform_random > percentage_unknown):
            nodelist[current_list_index][4].append([tag])   # set start tag for calculation
        else:
            if (tag == 0) and (uniform_random > percentage_unknown):
                nodelist[current_list_index][4].append([tag])   # set start tag for calculation
            else:
                nodelist[current_list_index][4].append([0, 1])   # set start tag for calculation
        # count FL & P:
        if tag == 0:
            leaf_distr[0] = leaf_distr[0] + 1
        else:
            leaf_distr[1] = leaf_distr[1] + 1
    else:
        min_depth = float('inf')
        max_depth = 0
        mean_depth = 0
        child_depth = 0
        for clade in subtree.clades:
            result = tag_tree(clade, nodelist, tag, leaf_distr, percentage_parasites, percentage_unknown, beta_distribution_parameters)
            clade = result[0]
            nodelist = result[1]
            leaf_distr = result[2]
            if result[3][0] < min_depth:
                min_depth = result[3][0]
            if result[3][1] > max_depth:
                max_depth = result[3][1]
            child_depth = child_depth + result[3][2]
        mean_depth = child_depth/len(subtree.clades) + 1
        depths = [min_depth + 1, max_depth + 1, mean_depth] 
    nodelist[current_list_index][1] = depths
    return [subtree, nodelist, leaf_distr, depths]

def get_non_binary_tree(subtree, nodelist):
    i = 0
    while i != len(subtree.clades):
        if subtree.clades[i].is_terminal():                 # is leave node?
            i += 1
        else:
            element = find_element_in_nodelist(subtree.clades[i].name, nodelist)
            limit = get_limit(element[1][2])
            # print('i=', i, 'len=', len(subtree.clades))
            new_random = uniform(0, 1)                      # choose if we want to delete ourselve
            # print(new_random, ' < ', limit)
            if new_random < limit:                          # or new_random < 0.9:
                # print('delete me!')
                subtree.clades += subtree.clades[i].clades  # add children
                del subtree.clades[i]                       # delete internal node
                # current clades: clade_1 clade_2 ... clade_i-1 clade_i ... clade:_n
                # add children of clade_i, delete clade_i
                # new clades:clade_1 clade_2 ... clade_i-1 child_clade_1 ... child_clade_m ... clade:_n
                # child_clade_1 is new clade i
            else:                                           # if we don't deleted ourselve go on with children
                get_non_binary_tree(subtree.clades[i], nodelist)    # otherwise the children are in the current clade array
                i += 1
            
    return

def get_limit(depth):
    limit = 1 - 1/((depth+3)/4)
    if limit < 0.1:
        limit = 0.1
    # print('depth=', depth, ' -> limit=', str(round(limit,3)))
    return limit
