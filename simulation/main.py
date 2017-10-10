import buildTree
import Parsimony
import Drawings

from Bio import Phylo
from copy import deepcopy

def main():
    """Main method"""
    number_trees = 1
    number_leafnodes = 16
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
        # Parsimony.parsimony(current_tree.clade)
        # Parsimony.parsimony(current_tree.clade, current_tree)
        
        # ---------------- drawings ----------------
        current_tree.name = 'random tree'
        Phylo.draw(current_tree)
        named_tree = deepcopy(current_tree)
        named_tree.name = 'tagged tree'
        Drawings.tag_names(named_tree.clade, nodelist)
        Phylo.draw(named_tree)
        untagged_tree = deepcopy(current_tree)
        untagged_tree.name = 'untagged tree'
        Drawings.tag_leaf_names(untagged_tree.clade, nodelist)
        Phylo.draw(untagged_tree)
        # current_tree.name = 'parsimonious solution tree'
        # Phylo.draw(current_tree)
        # Phylo.draw_graphviz(current_tree)
        # pylab.show()
    # save treelist in a newick file
    Phylo.write(binary_trees, 'originalTrees.tre', 'newick')


    return

main()
