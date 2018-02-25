import sys

from Bio import Phylo
from termcolor import colored

# input arguments
args = sys.argv

# values for simulation:
subtree_ott = sys.argv[1]

# subtree_otts = [['ott304358', 'Eukaryota'], ['ott361838', 'Chloroplastida'],
#         ['ott691846', 'Metazoa'], ['ott395057', 'Nematoda'], ['ott801601', 'Vertebrata'],
#         ['ott229562', 'Tetrapoda'], ['ott244265', 'Mammalia'], ['ott913935', 'Primates'],
#         ['ott770311', 'Hominidae'], ['ott352914', 'Fungi'], ['ott844192', 'Bacteria'],
#         ['ott996421', 'Archaea']]

# global variables
nr_internal_nodes = 0
nr_leaf_nodes = 0
origins = 0
losses = 0

def main():
    print(colored("---------------- read tree ----------------", "green"))
    tree = Phylo.read('./results/Eukaryota_tree-castor.tre', 'newick')
    
    print(colored("---------------- find subtrees ----------------", "green"))
    find_subtree(tree.clade)
    return

def find_subtree(subtree):
    # global subtree_ott
    global nr_internal_nodes
    global nr_leaf_nodes
    global origins
    global losses

    if not subtree.is_terminal():
        # subtree.name = ott $ index $ originaltag or $(finaltag)
        node = subtree.name.split('$')
        if node[0] == subtree_ott:
            print('Rootnode of this subtree has state: ', node[2])
            count_origins_and_losses(subtree, get_state(node[2]))
            print(subtree_ott, 'has', nr_internal_nodes, 'internal nodes and', nr_leaf_nodes, 'leaf_nodes')
            print(subtree_ott, 'has', origins, 'origins (FL -> P) and', losses, 'losses (P -> FL)')
        for clade in subtree.clades:
            find_subtree(clade)
    return

def count_origins_and_losses(subtree, father_state):
    global nr_internal_nodes
    global nr_leaf_nodes
    global origins
    global losses

    node = subtree.name.split('$')
    node_state = get_state(node[2])
    if node_state != father_state:
        if father_state == 0:
            origins += 1        # FL -> P
        else:
            losses += 1         # P -> FL

    if subtree.is_terminal():
        nr_leaf_nodes += 1
    else:
        nr_internal_nodes += 1
        for clade in subtree.clades:
            clade = count_origins_and_losses(clade, node_state)
    return subtree

def get_state(state):
    if state.startswith('('):
        # finaltag
        return int(state[1:-1])
    else:
        # originaltag
        return int(state) -1

main()
