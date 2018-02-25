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
            # Phylo.draw(subtree)
            print('Rootnode of this subtree has state: ', node[2])
            print(colored("---------------- count origins and losses ----------------", "green"))
            count_origins_and_losses(subtree, get_state(node[2]), False)
            print(subtree_ott, 'has', nr_internal_nodes, 'internal nodes and', nr_leaf_nodes, 'leaf_nodes')
            print(subtree_ott, 'has', origins, 'origins (FL -> P) and', losses, 'losses (P -> FL)')
        for clade in subtree.clades:
            find_subtree(clade)
    return

def count_origins_and_losses(subtree, father_state, found):
    global nr_internal_nodes
    global nr_leaf_nodes
    global origins
    global losses

    new_found = False

    node = subtree.name.split('$')
    node_state = get_state(node[2])
    if not  found:
        if node_state != father_state:
            print(node_state, father_state)
            if father_state == 0:
                origins += 1        # FL -> P
                new_found = True
            else:
                losses += 1         # P -> FL
                new_found = True

    if subtree.is_terminal():
        nr_leaf_nodes += 1
    else:
        nr_internal_nodes += 1
        found = False
        for clade in subtree.clades:
            found = count_origins_and_losses(clade, node_state, found)
    return new_found

def get_state(state):
    if state.startswith('('):
        # finaltag:     0 = FL, 1 = P
        # possible tags: 0, 0.333, 0.4, 0.5, 0.667, 0.75, 1
        # rounded to:    0  0      0    0    1      1     1
        return round(float(state[1:-1]))
    else:
        # originaltag:  1 = FL, 2 = P
        return round(float(state) -1)

main()
