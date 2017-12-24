"""This module builds a random binary tree and give tags to every node."""

import datetime
from copy import deepcopy

import matplotlib.pyplot as plt
from Bio import Phylo
from numpy import random

from utilities import Helpers

# global variables / parameters:
#   for freeliving_distribution
A_FL = 8.0
B_FL = 6.25
#   for parasite_distribution
A_P = 3
B_P = 8.0

freeliving_distribution = random.beta(a=A_FL, b=B_FL, size=5000)
parasite_distribution = random.beta(a=A_P, b=B_P, size=5000)

# the histogram of the data
n, bins, patches = plt.hist(parasite_distribution, 100, normed=1, facecolor='r', alpha=0.75)
n, bins, patches = plt.hist(freeliving_distribution, 100, normed=1, facecolor='b', alpha=0.75)

# plt.xlabel('Smarts')
# plt.ylabel('Probability')
plt.title('Histogram of distributions')
plt.text(0.5, 9, r'red: parasites, blue: free-living')
plt.axis([0, 1, 0, 10])
plt.grid(True)
plt.show()


def get_random_tagged_tree(number_leafnodes, percentage):
    """build a random binary tree fully tagged with FL and P"""
    # Arguments:
    #   number_leafnodes    - needed for randomized function
    #   percentage          - [realP, percentage_P, percentage_FL]

    START_TIME = datetime.datetime.now().replace(microsecond=0)
    CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)
    print("---- randomized tree ----")
    percentage_parasites = 0
    # randomized(cls, taxa, branch_length=1.0, branch_stdev=None) 
    #   Create a randomized bifurcating tree given a list of taxa.
    #   https://github.com/biopython/biopython/blob/master/Bio/Phylo/BaseTree.py
    randomized_tree = Phylo.BaseTree.Tree.randomized(number_leafnodes)
    randomized_tree.clade.name = 'root'
    boolean = True
    CURRENT_TIME = Helpers.print_time(START_TIME)
    print("---- tag tree ----")
    while boolean:
        current_tree = deepcopy(randomized_tree)
        result = tag_tree(current_tree.clade, [], 0, [0, 0], percentage) # father_tag = 0 -> free living
        nodelist = result[1]
        leaf_distr = result[2]
        # child_depth = child_depth + result[3]
        # %P = #FL / (#P + #FL) * 100
        percentage_parasites = leaf_distr[1] / (leaf_distr[0] + leaf_distr[1]) * 100
        print("tried", percentage_parasites, "% of parasites")  # 40% parasites?
        if (percentage[0] - 5) < percentage_parasites < (percentage[0] + 5):
            boolean = False
    print("----")
    CURRENT_TIME = Helpers.print_time(START_TIME)
    print("----")
    # print(percentage_parasites, '% parasites,', 100 - percentage_parasites, '% free-living')
    return [current_tree, nodelist]

def tag_tree(subtree, nodelist, father_tag, leaf_distr, percentage):
    """Function tags all nodes of a given (binary) subtree with names FL or P."""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    #   father_tag  - 0 or 1 (FL or P)
    #   leaf_distr  - [#FL, #P] - distribution of FL and P in the leave nodes
    #   percentage  - [realP, percentage_P, percentage_FL]
    depth = -1
    if father_tag == 0:
        # freeliving_distribution:
        new_random = random.beta(a=A_FL, b=B_FL)
    else:
        # parasite_distribution:
        new_random = random.beta(a=A_P, b=B_P)

    tag = 0         # -> FL
    if new_random < 0.4:
        tag = 1     # -> P
    #               [id, depth, originaltag, finaltag, calc[taglist]]
    nodelist.append([subtree.name, depth, tag, '', []])
    subtree.name = subtree.name + "$" + str(len(nodelist) - 1)
    current_list_index = len(nodelist) - 1
    # if leaf node, then depth = 1, set finaltag, increase leaf distribution
    if subtree.is_terminal():
        depth = 1
        uniform_random = random.uniform() # choose if we want to delete ourselve
        # unknown node?
        if (tag == 1) and (uniform_random <= percentage[1]):
            nodelist[current_list_index][4].append([tag])   # set start tag for calculation
        else:
            if (tag == 0) and (uniform_random <= percentage[2]):
                nodelist[current_list_index][4].append([tag])   # set start tag for calculation
            else:
                nodelist[current_list_index][4].append([0, 1])   # set start tag for calculation
        # count FL & P:
        if tag == 0:
            leaf_distr[0] = leaf_distr[0] + 1
        else:
            leaf_distr[1] = leaf_distr[1] + 1
    else:
        child_depth = 0
        for clade in subtree.clades:
            result = tag_tree(clade, nodelist, tag, leaf_distr, percentage)
            clade = result[0]
            nodelist = result[1]
            leaf_distr = result[2]
            child_depth = child_depth + result[3]
        depth = child_depth/len(subtree.clades) + 1 
    nodelist[current_list_index][1] = depth
    return [subtree, nodelist, leaf_distr, depth]
