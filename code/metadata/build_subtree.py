import sys
from copy import deepcopy

from Bio import Phylo
from termcolor import colored

# input arguments
args = sys.argv

# values from  input:
subtree_ott = sys.argv[1]
subtree_name = sys.argv[2]

# examples:
# subtree_otts+name = [['ott304358', 'Eukaryota'], ['ott361838', 'Chloroplastida'],
#         ['ott691846', 'Metazoa'], ['ott395057', 'Nematoda'], ['ott801601', 'Vertebrata'],
#         ['ott229562', 'Tetrapoda'], ['ott244265', 'Mammalia'], ['ott913935', 'Primates'],
#         ['ott770311', 'Hominidae'], ['ott352914', 'Fungi'], ['ott844192', 'Bacteria'],
#         ['ott996421', 'Archaea']]
index = 0
nr_internal_nodes = 0
nr_leaf_nodes = 0

def main():
    path_tree = "./data/opentree9.1_tree/labelled_supertree/labelled_supertree.tre"

    print(colored("---------------- read tree ----------------", "green"))
    tree = Phylo.read(path_tree, 'newick')
    
    print(colored("---------------- find subtrees ----------------", "green"))
    find_subtree(tree.clade)
    return

def find_subtree(subtree):
    global index
    global nr_internal_nodes
    global nr_leaf_nodes

    if not subtree.is_terminal():
        if subtree.name == subtree_ott:
            new_subtree = deepcopy(subtree)
            new_subtree = prepare_subtree(new_subtree)
            index = 0
            subtree_path = './data/subtree/' + subtree_name + '.tre'
            print("save tree at", subtree_path)
            Phylo.write(new_subtree, subtree_path, 'newick')
            print(subtree_name, 'has', nr_internal_nodes, 'internal nodes and', nr_leaf_nodes, 'leaf_nodes')
            nr_internal_nodes = 0
            nr_leaf_nodes = 0
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
