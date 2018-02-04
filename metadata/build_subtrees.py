from copy import deepcopy

from Bio import Phylo
from termcolor import colored

# global variables
subtree_otts = [['ott304358', 'Eukaryota'], ['ott352914', 'Fungi'], ['ott691846', 'Metazoa'], 
        ['ott395057', 'Nematoda'], ['ott801601', 'Vertebrata'], ['ott229562', 'Tetrapoda'], 
        ['ott244265', 'Mammalia'], ['ott913935', 'Primates'], ['ott770311', 'Hominidae'], 
        ['ott361838', 'Chloroplastida']]
index = 0
nr_internal_nodes = 0
nr_leaf_nodes = 0

def main():
    path_tree = "../data/opentree9.1_tree/labelled_supertree/labelled_supertree.tre"

    print(colored("---------------- read tree ----------------", "green"))
    tree = Phylo.read(path_tree, 'newick')
    
    print(colored("---------------- find subtrees ----------------", "green"))
    find_subtree(tree.clade)
    return

def find_subtree(subtree):
    global subtree_otts
    global index
    global nr_internal_nodes
    global nr_leaf_nodes
    if len(subtree_otts) == 0:
        return
    if not subtree.is_terminal():
        for item in subtree_otts:
            if subtree.name == item[0]:
                new_subtree = deepcopy(subtree)
                new_subtree = prepare_subtree(new_subtree)
                index = 0
                subtree_path = '../data/subtree/' + item[1] + '.tre'
                print("save tree at", subtree_path)
                Phylo.write(new_subtree, subtree_path, 'newick')
                print(item[1], 'has', nr_internal_nodes, 'internal nodes and', nr_leaf_nodes, 'leaf_nodes')
                nr_internal_nodes = 0
                nr_leaf_nodes = 0
                subtree_otts.remove(item)
        for clade in subtree.clades:
            find_subtree(clade)
    return

def prepare_subtree(subtree):
    global index
    global nr_internal_nodes
    global nr_leaf_nodes
    # For the quicker finding of the element in the nodelist of the accociated node.
    subtree.name = subtree.name + "$" + str(index)
    index += 1
    if subtree.is_terminal():
        nr_leaf_nodes += 1
    else:
        nr_internal_nodes += 1
        for clade in subtree.clades:
            clade = prepare_subtree(clade)
    return subtree
    
main()
