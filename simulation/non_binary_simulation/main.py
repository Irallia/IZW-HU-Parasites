"""main method"""

from copy import deepcopy
from pprint import pprint

from Bio import Phylo

import buildTree
from parsimony.Fitch_MP import fitch_parsimony
from parsimony.My_MP import my_parsimony
from parsimony.Sankoff_MP import sankoff_parsimony
import Drawings

def main():
    """Main method"""
    number_trees = 5    # number of simulated trees
    number_leafnodes = 100
    percentage = 40   # percentage of parasites (percentage +-5%)

    print("Build", number_trees, "random trees with", number_leafnodes, "leafnodes", percentage, "parasites.")
    # TODO: unknown nodes!!

    for _ in range(0, number_trees):
        result = buildTree.get_random_tagged_tree(number_leafnodes, percentage)
        current_tree = result[0]
        nodelist = result[1]
        # Phylo.draw(current_tree)
        # ---------------- non-binary tree ----------------
        buildTree.get_non_binary_tree(current_tree.clade, nodelist)
        # Phylo.draw(current_tree)
        # ---------------- maximum parsimony algorithms ----------------
        list_of_nodelists = run_parsimony_algorithms(current_tree, nodelist)
        # ---------------- compare results ----------------
        # ---------------- drawings ----------------
        # do_some_drawings(current_tree, nodelist, parsimony_tree, parsimony_nodelist)

    # save treelist in a newick file
    # Phylo.write(binary_trees, 'originalTrees.tre', 'newick')
    return

def run_parsimony_algorithms(current_tree, nodelist):
    fitch_MP_nodelists = []
    my_MP_nodelists = []
    sankoff_MP_nodelists = []
    # ---------------- Fitch parsimony ----------------
    fitch_MP_tree = deepcopy(current_tree)
    fitch_MP_nodelist = deepcopy(nodelist)
    fitch_parsimony(fitch_MP_tree.clade, fitch_MP_nodelist)
    fitch_MP_nodelists.append(fitch_MP_nodelist)
    # ---------------- my parsimony ----------------
    my_MP_tree = deepcopy(current_tree)
    my_MP_nodelist = deepcopy(nodelist)
    # my_parsimony(my_MP_tree.clade, my_MP_nodelist)
    my_MP_nodelists.append(my_MP_nodelists)
    # ---------------- Sankoff parsimony ----------------
    sankoff_MP_tree = deepcopy(current_tree)
    sankoff_MP_nodelist = deepcopy(nodelist)
    sankoff_parsimony(sankoff_MP_tree.clade, sankoff_MP_nodelist)
    sankoff_MP_nodelists.append(sankoff_MP_nodelist)
    return [fitch_MP_nodelists, my_MP_nodelists, sankoff_MP_nodelists]

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
