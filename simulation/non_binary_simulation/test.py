"""main method"""

from copy import deepcopy
from pprint import pprint
from random import gauss

from Bio import Phylo

import buildTree

VARIANCE = 0.5

def set_limits(subtree, nodelist, depth):
    limit = 0.9
    for clade in subtree.clades:
        if not clade.is_terminal():
            # print('-- go deeper --')
            depth = set_limits(clade, nodelist, depth)
            depth = depth + 0.25
            limit = 1-1/depth
            clade.name = str(round(limit,3))
        else:
            depth = 1
    return depth

def un_binary_tree(subtree, new_random):
    for clade in subtree.clades:
        if not clade.is_terminal():
            # print('-- go deeper --')
            un_binary_tree(clade, new_random)
    i = 0
    while i != len(subtree.clades):
        if subtree.clades[i].is_terminal():
            i += 1
        else:
            limit = float(subtree.clades[i].name)
            print('i=', i)
            new_random = min(1, max(0, gauss(new_random, VARIANCE))) # choose if we want to delete ourselve
            print(new_random, ' < ', limit)
            if new_random < limit: # or new_random < 0.9:
                print('delete me!')
                subtree.clades += subtree.clades[i].clades # add children
                del subtree.clades[i]   # delete internal node
            else:
                i += 1
    return


def main():
    """Main method"""
    number_leafnodes = 80
    lower_range = 35
    upper_range = 45
    result = buildTree.get_random_tagged_tree(number_leafnodes, lower_range, upper_range)
    tree = result[0]
    nodelist = result[1]
    tree.name = 'tree'
    Phylo.draw(tree)
    changed_tree = deepcopy(tree)
    set_limits(changed_tree.clade, [], -1)
    changed_tree.name = 'tree with limits'
    Phylo.draw(changed_tree)
    un_binary_tree(changed_tree.clade, 0.5)
    changed_tree.name = 'not binary tree'
    Phylo.draw(changed_tree)
    return

main()

