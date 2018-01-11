"""main method"""
import csv
import datetime
import sys
from copy import deepcopy
from pprint import pprint
from time import gmtime, strftime

import matplotlib.pyplot as plt
from Bio import Phylo
from numpy import random
from termcolor import colored

from find_best_betadist import buildTree

# input arguments
args = sys.argv

# fix numbers:
leaf_nodes = 2300000        # 2 300 000 Eukaryota
number_P = 43674
number_FL = 88967

# values for simulation:
number_trees = int(sys.argv[2])  # number of simulated trees
number_leafnodes = int(sys.argv[1])

def main():
    """Main method"""
    global START_TIME
    global CURRENT_TIME
    #               [percentage parasites, A_FL, B_FL, A_P, B_P]
    beta_distribution_parameters = [0.4, 8.0, 6.25, 3.0, 8.0]   # 40 P - 60 FL
    # beta_distribution_parameters = [0.5, 7.0, 3.5, 3.5, 7.0]    # 50 P - 50 FL
    realP = beta_distribution_parameters[0]*100                 # percentage of parasites (percentage +-2%)

    # -------------------------------------plot distribution------------------------------------
    #   for freeliving_distribution
    A_FL = beta_distribution_parameters[1]
    B_FL = beta_distribution_parameters[2]
    #   for parasite_distribution
    A_P = beta_distribution_parameters[3]
    B_P = beta_distribution_parameters[4]
    freeliving_distribution = random.beta(a=A_FL, b=B_FL, size=5000)
    parasite_distribution = random.beta(a=A_P, b=B_P, size=5000)

    # the histogram of the data
    n, bins, patches = plt.hist(parasite_distribution, 100, normed=1, facecolor='r', alpha=0.75)
    n, bins, patches = plt.hist(freeliving_distribution, 100, normed=1, facecolor='b', alpha=0.75)

    # plt.xlabel('Smarts')
    # plt.ylabel('Probability')
    plt.title('Histogram of distributions')
    plt.text(0.5, 9, r'red: parasites, blue: free-living')
    plt.axis([0, 1, 0, 10])
    plt.grid(True)
    plt.show()
    #-------------------------------------------------------------------------------------------

    print(colored("------------------------ start ------------------------", "green"))
    print(colored("---------------- metadata ----------------", "green"))
    diffs = [["Fitch", "My", "Sankoff"]]
    print("real OTL tree: 2500000 nodes: 240000 internal,", leaf_nodes, "leaf nodes")
    print("Information about species from GloBI:", number_P, "#P,", number_FL, "#FL")
    percentage_P = 1 / leaf_nodes * number_P
    percentage_FL = 1 / leaf_nodes * number_FL
    percentage_U = 1 - percentage_P - percentage_FL
    print("Original Values:")
    print("=>", round(percentage_P * 100, 2), "% parasites,", round(percentage_FL * 100, 2), "% freeliving =>", round(percentage_U * 100, 2), "% unknown leaf nodes")
    percentage = [realP, percentage_P, percentage_FL]
    print("Build", colored(number_trees, 'blue'), "random trees with", colored(number_leafnodes, 'blue'), "leafnodes", colored(realP, 'blue'), "% parasites.")
    print(colored("---------------- trees ----------------", "green"))
    for i in range(1, number_trees + 1):
        print("Tree", colored(i, 'red'))
        result = buildTree.get_random_tagged_tree(number_leafnodes, percentage, beta_distribution_parameters)
        current_tree = result[0]
        nodelist = result[1]
    return

main()
