"""main method"""
import csv
import datetime
import sys
from copy import deepcopy
from pprint import pprint
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored

from find_best_betadist import buildTree
from utilities import Drawings, Helpers

# input arguments
args = sys.argv

# global variables:
START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)

# fix numbers:
leaf_nodes = 2300000        # 2 300 000 Eukaryota
number_P = 43674
number_FL = 88967

# values for simulation:
number_trees = int(sys.argv[2])  # number of simulated trees
number_leafnodes = int(sys.argv[1])
realP = 40                  # percentage of parasites (percentage +-5%)

def main():
    """Main method"""
    global START_TIME
    global CURRENT_TIME
    print(colored("------------------------ start simulation ------------------------", "green"))
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    CURRENT_TIME = Helpers.print_time(START_TIME)
    print(colored("---------------- metadata ----------------", "green"))
    diffs = [["Fitch", "My", "Sankoff"]]
    print("real OTL tree: 2500000 nodes: 240000 internal,", leaf_nodes, "leaf nodes")
    print("Information about species from GloBI:", number_P, "#P,", number_FL, "#FL")
    percentage_P = 1 / leaf_nodes * number_P
    percentage_FL = 1 / leaf_nodes * number_FL
    percentage_U = 1 - percentage_P - percentage_FL
    print("=>", round(percentage_P * 100, 2), "% parasites,", round(percentage_FL * 100, 2), "% freeliving =>", round(percentage_U * 100, 2), "% unknown leaf nodes")
    percentage = [realP, percentage_P, percentage_FL]
    print("Build", colored(number_trees, 'blue'), "random trees with", colored(number_leafnodes, 'blue'), "leafnodes", colored(realP, 'blue'), "% parasites.")
    for i in range(1, number_trees + 1):
        print("Tree", colored(i, 'red'))
        print(colored("---------------- get random tree ----------------", "green"))
        result = buildTree.get_random_tagged_tree(number_leafnodes, percentage)
        current_tree = result[0]
        nodelist = result[1]
        CURRENT_TIME = Helpers.print_time(CURRENT_TIME)
    return

main()
