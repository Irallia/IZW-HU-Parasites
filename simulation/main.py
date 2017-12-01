"""main method"""

import csv
import datetime
from copy import deepcopy
from pprint import pprint
from time import gmtime, strftime

from Bio import Phylo

from non_binary_simulation import buildTree
from non_binary_simulation.parsimony.Fitch_MP import fitch_parsimony
from non_binary_simulation.parsimony.My_MP import my_parsimony
from non_binary_simulation.parsimony.Sankoff_MP import sankoff_parsimony
from utilities import Drawings

START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)


def main():
    """Main method"""
    global START_TIME
    global CURRENT_TIME
    print("------------------------ start simulation ------------------------")
    CURRENT_TIME = print_time(START_TIME)

    number_trees = 1    # number of simulated trees
    number_leafnodes = 40000
    percentage = 40   # percentage of parasites (percentage +-5%)

    print("Build", number_trees, "random trees with", number_leafnodes, "leafnodes", percentage, "% parasites.")
    # TODO: unknown nodes!!

    for _ in range(0, number_trees):
        print("---------------- get random tree ----------------")
        result = buildTree.get_random_tagged_tree(number_leafnodes, percentage)
        current_tree = result[0]
        nodelist = result[1]
        # Phylo.draw(current_tree)
        CURRENT_TIME = print_time(CURRENT_TIME)
        print("---------------- multifurcate tree ----------------")
        buildTree.get_non_binary_tree(current_tree.clade, nodelist)
        # Phylo.draw(current_tree)
        CURRENT_TIME = print_time(CURRENT_TIME)
        print("---------------- maximum parsimony algorithms ----------------")
        run_parsimony_algorithms(current_tree, nodelist)
        # ---------------- compare results ----------------
        CURRENT_TIME = print_time(CURRENT_TIME)
        print("-------- evaluation --------")
        # ---------------- drawings ----------------
        # do_some_drawings(current_tree, nodelist, parsimony_tree, parsimony_nodelist)
        time_new = datetime.datetime.now().replace(microsecond=0)
        print("whole time needed:", time_new - START_TIME)
    return

def run_parsimony_algorithms(current_tree, nodelist):
    global START_TIME
    global CURRENT_TIME
    CURRENT_TIME = print_time(CURRENT_TIME)
    print("---------------- Fitch parsimony ----------------")
    fitch_MP_tree = deepcopy(current_tree)
    fitch_MP_nodelist = deepcopy(nodelist)
    fitch_parsimony(fitch_MP_tree.clade, fitch_MP_nodelist)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print("---------------- my parsimony ----------------")
    my_MP_tree = deepcopy(current_tree)
    my_MP_nodelist = deepcopy(nodelist)
    my_parsimony(my_MP_tree.clade, my_MP_nodelist)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print("---------------- Sankoff parsimony ----------------")
    sankoff_MP_tree = deepcopy(current_tree)
    sankoff_MP_nodelist = deepcopy(nodelist)
    sankoff_parsimony(sankoff_MP_tree, sankoff_MP_nodelist)
    CURRENT_TIME = print_time(CURRENT_TIME)
    # --------------------------------------------------------
    result_list = []
    for i in range(0, len(nodelist)):
        if fitch_MP_nodelist[i][3] == '':
            fitch_MP_nodelist[i][3] = '-'
        if my_MP_nodelist[i][3] == '':
            my_MP_nodelist[i][3] = '-'
        if sankoff_MP_nodelist[i][3] == '':
            sankoff_MP_nodelist[i][3] = '-'
        result_list.append([nodelist[i][0], nodelist[i][2], fitch_MP_nodelist[i][3], my_MP_nodelist[i][3], sankoff_MP_nodelist[i][3]])

    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result_list)
    # pprint(result_list)
    return

def do_some_drawings(tree, nodelist, parsimony_tree, parsimony_nodelist):
    """seperated drawings"""
    tree.name = 'random tree'
    # Phylo.draw(tree)
    named_tree = deepcopy(tree)
    named_tree.name = 'tagged tree'
    Drawings.tag_names(named_tree.clade, nodelist, 1)
    Phylo.draw(named_tree)
    untagged_tree = deepcopy(tree)
    untagged_tree.name = 'untagged tree'
    Drawings.tag_leaf_names(untagged_tree.clade, nodelist)
    # Phylo.draw(untagged_tree)
    # tree.name = 'parsimony down'
    # Phylo.draw(tree)
    # tree.name = 'parsimony up'
    # Phylo.draw(tree)
    parsimony_tree.name = 'parsimonious solution tree'
    Drawings.tag_names(parsimony_tree.clade, parsimony_nodelist, 2)
    Phylo.draw(parsimony_tree)
    parsimony_like_tree = deepcopy(tree)
    parsimony_like_tree.name = 'parsimonious-like solution tree'
    Drawings.tag_names(parsimony_like_tree.clade, nodelist, 2)
    Phylo.draw(parsimony_like_tree)
    # Phylo.draw_graphviz(parsimony_tree)
    # pylab.show()


def print_time(time_old):
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    time_new = datetime.datetime.now().replace(microsecond=0)
    print("time needed:", time_new - time_old)
    return time_new

main()
