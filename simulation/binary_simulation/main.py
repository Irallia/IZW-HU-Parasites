"""main method"""

from copy import deepcopy
from pprint import pprint

from Bio import Phylo

import buildTree
import Parsimony
import Parsimony_like
import Drawings

def main():
    """Main method"""

    number_trees = 5
    number_leafnodes = 20
    lower_range = 35
    upper_range = 45
    binary_trees = []
    for _ in range(0, number_trees):
        result = buildTree.get_random_tagged_tree(number_leafnodes, lower_range, upper_range)
        current_tree = result[0]
        nodelist = result[1]
        # print(nodelist)
        binary_trees.append(current_tree)
        # ---------------- parsimony ----------------
        parsimony_tree = deepcopy(current_tree)
        parsimony_nodelist = deepcopy(nodelist)
        Parsimony.parsimony(parsimony_tree.clade, parsimony_nodelist)
        # pprint(nodelist)
        # ---------------- parsimony like ----------------
        Parsimony_like.parsimony_like(current_tree.clade, nodelist)
        # pprint(nodelist)
        # ---------------- drawings ----------------
        do_some_drawings(current_tree, nodelist, parsimony_tree, parsimony_nodelist)

    # save treelist in a newick file
    # Phylo.write(binary_trees, 'originalTrees.tre', 'newick')
    return

def do_some_drawings(tree, nodelist, parsimony_tree, parsimony_nodelist):
    """seperated drawings"""
    tree.name = 'random tree'
    # Phylo.draw(tree)
    named_tree = deepcopy(tree)
    named_tree.name = 'tagged tree'
    Drawings.tag_names(named_tree.clade, nodelist, 1)
    Phylo.draw(named_tree)
    untagged_tree = deepcopy(tree)
    untagged_tree.name = 'untagged tree'
    Drawings.tag_leaf_names(untagged_tree.clade, nodelist)
    # Phylo.draw(untagged_tree)
    # tree.name = 'parsimony down'
    # Phylo.draw(tree)
    # tree.name = 'parsimony up'
    # Phylo.draw(tree)
    parsimony_tree.name = 'parsimonious solution tree'
    Drawings.tag_names(parsimony_tree.clade, parsimony_nodelist, 2)
    Phylo.draw(parsimony_tree)
    parsimony_like_tree = deepcopy(tree)
    parsimony_like_tree.name = 'parsimonious-like solution tree'
    Drawings.tag_names(parsimony_like_tree.clade, nodelist, 2)
    Phylo.draw(parsimony_like_tree)
    # Phylo.draw_graphviz(parsimony_tree)
    # pylab.show()

main()
