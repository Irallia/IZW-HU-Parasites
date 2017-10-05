import buildTree
import Parsimony

from Bio import Phylo

def main():
    """Main method"""
    number_trees = 1
    number_leafnodes = 16
    lower_range = 35
    upper_range = 45
    binary_original_trees = []
    binary_leaf_tagged_trees = []
    binary_parsimony_solution = []
    for _ in range(0, number_trees):
        current_tree = buildTree.get_random_tagged_tree(number_leafnodes, lower_range, upper_range)
        Phylo.draw(current_tree)
        binary_original_trees.append(current_tree)
        # untag internal nodes
        buildTree.untag_tree(current_tree.clade)
        current_tree.name = 'untagged tree'
        Phylo.draw(current_tree)
        binary_leaf_tagged_trees.append(current_tree)
        # parsimony
        Parsimony.parsimony(current_tree.clade)
        # Parsimony.parsimony(current_tree.clade, current_tree)
        current_tree.name = 'parsimonious solution tree'
        Phylo.draw(current_tree)
        # Phylo.draw_graphviz(current_tree)
        # pylab.show()
        binary_parsimony_solution.append(current_tree)
    # save treelist in a newick file
    # Phylo.write(current_tree, 'current_tree.tre', 'newick')
    Phylo.write(binary_original_trees, 'originalTrees.tre', 'newick')
    return

main()
