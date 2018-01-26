from Bio import Phylo
from termcolor import colored

# global variables
subtree_otts = [['ott304358', 'Eukaryota'], ['ott352914', 'Fungi'], ['ott691846', 'Metazoa'], 
        ['ott395057', 'Nematoda'], ['ott801601', 'Vertebrata'], ['ott229562', 'Tetrapoda'], 
        ['ott244265', 'Mammalia'], ['ott913935', 'Primates'], ['ott770311', 'Hominidae'], 
        ['ott361838', 'Chloroplastida']]

def main():
    path_tree = "../data/opentree9.1_tree/labelled_supertree/labelled_supertree.tre"

    print(colored("---------------- read tree ----------------", "green"))
    tree = Phylo.read(path_tree, 'newick')
    
    print(colored("---------------- find subtrees ----------------", "green"))
    find_subtree(tree.clade)
    return

def find_subtree(subtree):
    global subtree_otts
    if len(subtree_otts) == 0:
        return
    if not subtree.is_terminal():
        for item in subtree_otts:
            if subtree.name == item[0]:
                subtree_path = '../data/subtree/' + item[1] + '.tre'
                print("save tree at", subtree_path)
                Phylo.write(subtree, subtree_path, 'newick')
                subtree_otts.remove(item)
                print(subtree_otts)
        for clade in subtree.clades:
            find_subtree(clade)
    return
    
main()
