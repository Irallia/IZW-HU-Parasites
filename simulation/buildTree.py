import random
import pylab

# StringIO no longer exists in 3.x. Use either io.StringIO for text or io.BytesIO for bytes.
# from cStringIO import StringIO
from io import StringIO
from Bio import Phylo

# global variables / parameters:
VARIANCE = 0.2
ROOTNODEVALUE = 0.7


def tag_tree(subtree, random_number, leaf_dist):
    """Function tags all nodes of a given (binary) subtree with names FL or P."""
    # Arguments:
    #   subtree
    #   random_number - in [0, 1]
    #   leaf_dist     - [#FL, #P]
    id = '0'
    if subtree.name:
        id = subtree.name
    if random_number >= 0.5:
        subtree.name = id + '-FL'
    else:
        subtree.name = id + '-P'
    if subtree.is_terminal():
        if subtree.name.split('-')[1] == 'FL':
            leaf_dist[0] = leaf_dist[0] + 1
        else:
            leaf_dist[1] = leaf_dist[1] + 1
    else:
        for clade in subtree.clades:
            # random.gauss(mu, sigma) -> Gaussian distribution, mu: mean, sigma: standard deviation.
            new_random = min(1, max(0, random.gauss(random_number, VARIANCE)))
            leaf_dist = tag_tree(clade, new_random, leaf_dist)
    return leaf_dist

def untag_tree(subtree):
    """Function untags all internal nodes."""
    # Arguments:
    #   subtree
    if not subtree.is_terminal():
        subtree.name = subtree.name.split('-')[0]
        for clade in subtree.clades:
            untag_tree(clade)
    return

def parsimony(subtree, tree):
    # down:
    parsimony_down(subtree)
    tree.name = 'parsimony down'
    Phylo.draw(tree)
    # up:
    parsimony_up(subtree.clades[0], subtree.name, subtree.clades[1].name)
    parsimony_up(subtree.clades[1], subtree.name, subtree.clades[0].name)
    tree.name = 'parsimony up'
    Phylo.draw(tree)
    # final:
    parsimony_final(subtree)
    return

def parsimony_down(subtree):
    clade0_name = subtree.clades[0].name.split('-')
    clade1_name = subtree.clades[1].name.split('-')
    if len(clade0_name) == 1:
        parsimony_down(subtree.clades[0])
        clade0_name = subtree.clades[0].name.split('-')
    if len(clade1_name) == 1:
        parsimony_down(subtree.clades[1])
        clade1_name = subtree.clades[1].name.split('-')
    l_tag = clade0_name[1]
    r_tag = clade1_name[1]
    shared = False
    # RULE 1: share any states in common -> assign shared states
    if ('FL' in l_tag) & ('FL' in r_tag):
        subtree.name = subtree.name + '-FL'
        shared = True
    if ('P' in l_tag) & ('P' in r_tag):
        if shared:
            subtree.name = subtree.name + '&P'
        else:
            subtree.name = subtree.name + '-P'
        shared = True
    # RULE 2: no shared states -> assign union of states
    if not shared:
        subtree.name = subtree.name + '-FL&P'
    return

def parsimony_up(subtree, parent_name, siblings_name):
    if not subtree.is_terminal():
        p_tag_1 = parent_name.split('-')[1]
        p_tag_2 = 'FL&P'
        if  len(parent_name.split('-')) > 2:
            p_tag_2 = parent_name.split('-')[2]
        s_tag_1 = siblings_name.split('-')[1]
        s_tag_2 = 'FL&P'
        if len(siblings_name.split('-')) > 2:
            s_tag_2 = siblings_name.split('-')[2]
        shared = False
        # RULE 1: share any states in common -> assign shared states
        if ('FL' in p_tag_1) & ('FL' in p_tag_2) & ('FL' in s_tag_1) & ('FL' in s_tag_2):
            subtree.name = subtree.name + '-FL'
            shared = True
        if ('P' in p_tag_1) & ('P' in p_tag_2) & ('P' in s_tag_1) & ('P' in s_tag_2):
            if shared:
                subtree.name = subtree.name + '&P'
            else:
                subtree.name = subtree.name + '-P'
            shared = True
        # RULE 2: no shared states -> assign union of states
        if not shared:
            subtree.name = subtree.name + '-FL&P'
        # go on with children
        parsimony_up(subtree.clades[0], subtree.name, subtree.clades[1].name)
        parsimony_up(subtree.clades[1], subtree.name, subtree.clades[0].name)
    return

def parsimony_final(subtree):
    if not subtree.is_terminal():
        tags = subtree.name.split('-')
        if len(tags) > 2:
            shared = False
            # RULE 1: share any states in common -> assign shared states
            if ('FL' in tags[1]) & ('FL' in tags[2]):
                subtree.name = tags[0] + '-FL'
                # subtree._set_color('blue')
                shared = True
            if ('P' in tags[1]) & ('P' in tags[2]):
                if shared:
                    subtree.name = subtree.name + '&P'
                    # subtree._set_color('magenta')
                else:
                    subtree.name = tags[0] + '-P'
                    # subtree._set_color('red')
                shared = True
            # RULE 2: no shared states -> assign union of states
            if not shared:
                subtree.name = tags[0] + '-FL&P'
                # subtree._set_color('magenta')
    # go on with children
    if not subtree.is_terminal():
        parsimony_final(subtree.clades[0])
        parsimony_final(subtree.clades[1])
    return

def main():
    """Main method"""
    number_trees = 1
    number_leafnodes = 16
    binary_original_trees = []
    binary_leaf_tagged_trees = []
    binary_parsimony_solution = []
    for _ in range(0, number_trees):
        # randomized(cls, taxa, branch_length=1.0, branch_stdev=None) 
        #   Create a randomized bifurcating tree given a list of taxa.
        #   https://github.com/biopython/biopython/blob/master/Bio/Phylo/BaseTree.py
        # build a random binary trees
        current_tree = Phylo.BaseTree.Tree()
        percentage_parasites = 0
        boolean = True
        while boolean:
            # 40% parasites?
            current_tree = Phylo.BaseTree.Tree.randomized(number_leafnodes)
            current_tree.name = 'random tree'
            Phylo.draw(current_tree)
            leaf_distr = tag_tree(current_tree.clade, ROOTNODEVALUE, [0, 0])
            percentage_parasites = leaf_distr[1] / (leaf_distr[0] + leaf_distr[1]) * 100
            if 35 < percentage_parasites < 45:
                boolean = False
        print(percentage_parasites, '% parasites,', 100 - percentage_parasites, '% free-living')
        current_tree.name = 'tagged tree'
        Phylo.draw(current_tree)
        binary_original_trees.append(current_tree)
        # untag internal nodes
        untag_tree(current_tree.clade)
        current_tree.name = 'untagged tree'
        Phylo.draw(current_tree)
        binary_leaf_tagged_trees.append(current_tree)
        # parsimony
        parsimony(current_tree.clade, current_tree)
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