"""main method"""

from copy import deepcopy
from pprint import pprint
from random import gauss

from Bio import Phylo

import buildTree

VARIANCE = 0.5

def un_binary_tree(subtree, new_random):
    # Phylo.draw(subtree)
    i = 0
    while i != len(subtree.clades):
        print(i)
        new_random = min(1, max(0, gauss(new_random, VARIANCE))) # choose if we want to delete ourselve
        print(new_random)
        if new_random > 0.5:
            print('delete me!')
            subtree.clades += subtree.clades[i].clades # add children
            del subtree.clades[i]   # delete internal node
        else:
            i += 1
    for clade in subtree.clades:
        if not clade.is_terminal():
            print('-- go deeper --')
            un_binary_tree(clade, new_random)
    return


def main():
    """Main method"""
    number_leafnodes = 20
    lower_range = 35
    upper_range = 45
    result = buildTree.get_random_tagged_tree(number_leafnodes, lower_range, upper_range)
    tree = result[0]
    nodelist = result[1]
    tree.name = 'tree'
    Phylo.draw(tree)
    changed_tree = deepcopy(tree)
    un_binary_tree(changed_tree.clade, 0.5)
    changed_tree.name = 'not binary tree'
    Phylo.draw(changed_tree)
    return

main()

