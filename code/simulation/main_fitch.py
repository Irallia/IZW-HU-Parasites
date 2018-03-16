"""main method"""
import csv
import datetime
import sys
from code.simulation.non_binary_simulation import buildTree
from code.simulation.non_binary_simulation.parsimony.Fitch_MP import \
    fitch_parsimony

from code.utilities.Helpers import print_time
from copy import deepcopy
from pprint import pprint
from time import gmtime, strftime

from Bio import Phylo
from termcolor import colored

# input arguments
args = sys.argv

# global variables:
START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)

# values for simulation:
number_leafnodes = int(sys.argv[1])
number_trees = int(sys.argv[2])                 # number of simulated trees
percentage_parasites = float(sys.argv[3])       # between 0 and 1
percentage_unknown = float(sys.argv[4])         # between 0 and 1
percentage_multifurcation = float(sys.argv[5])  # between 0 and 1

def main():
    """Main method"""
    global START_TIME
    global CURRENT_TIME
    print(colored("------------------------ start simulation ------------------------", "green"))
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    CURRENT_TIME = print_time(START_TIME)
    print(colored("---------------- metadata ----------------", "green"))
    metadata()
    print(colored("---------------- parameters ----------------", "green"))
    print("Simulate", colored(number_trees, 'blue'), "random trees with", 
        colored(number_leafnodes, 'blue'), "leafnodes", 
        colored(percentage_parasites*100, 'blue'), "% parasites and",
        colored(percentage_unknown*100, 'blue'), "% unknown leafnodes and",
        colored(percentage_multifurcation*100, 'blue'), "% of multifurcation of the internal nodes.")
        beta_distribution_parameters = decide_for_beta_distribution_parameters(percentage_parasites)
    print(beta_distribution_parameters)
    diffs = [["Fitch1", "Fitch2", "Fitch3", "Fitch4"]]
    for i in range(1, number_trees + 1):
        print("Tree", colored(i, 'red'))
        print(colored("---------------- get random tree ----------------", "green"))
        result = buildTree.get_random_tagged_tree(number_leafnodes, percentage_parasites, percentage_unknown, percentage_multifurcation, beta_distribution_parameters)
        current_tree = result[0]
        nodelist = result[1]
        # CURRENT_TIME = print_time(CURRENT_TIME)
        print(colored("---------------- multifurcate tree ----------------", "green"))
        buildTree.get_non_binary_tree(current_tree.clade, nodelist)
        CURRENT_TIME = print_time(CURRENT_TIME)
        print(colored("---------------- maximum parsimony algorithms ----------------", "green"))
        diff_percentage = run_parsimony_algorithms(current_tree, nodelist)
        diffs.append(diff_percentage)
        time_new = datetime.datetime.now().replace(microsecond=0)
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        print("whole time needed:", time_new - START_TIME)
        print(colored("--------------------------------", "red"))

    f_dif1 = 0.0
    f_dif2 = 0.0
    f_dif3 = 0.0
    f_dif4 = 0.0
    for i in range(1, number_trees + 1):
        f_dif1 += float(diffs[i][0])
        f_dif2 += float(diffs[i][1])
        f_dif3 += float(diffs[i][2])
        f_dif4 += float(diffs[i][3])
    f_dif1 = round(f_dif1 / number_trees, 2)
    f_dif2 = round(f_dif2 / number_trees, 2)
    f_dif3 = round(f_dif3 / number_trees, 2)
    f_dif4 = round(f_dif4 / number_trees, 2)

    row = [percentage_unknown, f_dif1, f_dif2, f_dif3, f_dif4]
    csv_title = "data/simulation/fitch" + str(int(percentage_parasites*100)) + "-unknown" + str(int(percentage_multifurcation*100)) + "-multifurcation.csv"
    fp = open(csv_title, 'a')
    writer = csv.writer(fp)
    writer.writerow((row)) 
    fp.close()
    print("saved in:")
    print(csv_title)

    print(colored("--------------------------------", "green"))
    print(colored(number_trees, 'blue'), " trees simulated with", 
        colored(number_leafnodes, 'blue'), "leafnodes", 
        colored(percentage_parasites*100, 'blue'), "% parasites and",
        colored(percentage_unknown*100, 'blue'), "% unknown leafnodes and",
        colored(percentage_multifurcation*100, 'blue'), "% of multifurcation of the internal nodes.")
    print("correctly predicted (including already known leaf nodes):")
    print("differences Fitch1 / Fitch2 / Fitch3 / Fitch4")
    percentage_correctly_predicted = "| " + str(f_dif1) +" % | " + str(f_dif2) + " % | " + str(f_dif3) + " % |" + str(f_dif4) + " % |"
    print(colored(percentage_correctly_predicted, 'red'))
    print(colored("--------------------------------", "green"))
    return

def run_parsimony_algorithms(current_tree, nodelist):
    global START_TIME
    global CURRENT_TIME
    CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)
    print(colored("---------------- Fitch1 parsimony ----------------", "green"))
    fitch_MP_tree1 = deepcopy(current_tree)
    fitch_MP_nodelist1 = deepcopy(nodelist)
    fitch_parsimony(fitch_MP_tree1.clade, fitch_MP_nodelist1, 1)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- Fitch2 parsimony ----------------", "green"))
    fitch_MP_tree2 = deepcopy(current_tree)
    fitch_MP_nodelist2 = deepcopy(nodelist)
    fitch_parsimony(fitch_MP_tree2.clade, fitch_MP_nodelist2, 2)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- Fitch3 parsimony ----------------", "green"))
    fitch_MP_tree3 = deepcopy(current_tree)
    fitch_MP_nodelist3 = deepcopy(nodelist)
    fitch_parsimony(fitch_MP_tree3.clade, fitch_MP_nodelist3, 3)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- Fitch4 parsimony ----------------", "green"))
    fitch_MP_tree4 = deepcopy(current_tree)
    fitch_MP_nodelist4 = deepcopy(nodelist)
    fitch_parsimony(fitch_MP_tree4.clade, fitch_MP_nodelist4, 4)
    CURRENT_TIME = print_time(CURRENT_TIME)
    # --------------------------------------------------------
    print(colored("-------- evaluation --------", "green"))
    differences = evaluation(nodelist, fitch_MP_nodelist1, fitch_MP_nodelist2, fitch_MP_nodelist3, fitch_MP_nodelist4)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("--------------------------------", "green"))
    return differences

def decide_for_beta_distribution_parameters(percentage_parasites):
                                # [A_FL, B_FL, A_P, B_P]
    beta_distribution_parameters = [7, 3.5, 3.5, 7]   # 40 P - 60 FL

    # decide for distribution:
    if percentage_parasites == 0.1:
        beta_distribution_parameters = [7, 24, 0.5, 7]     # 10 P - 90 FL
    elif percentage_parasites == 0.2:
        beta_distribution_parameters = [7, 13.25, 1.25, 7] # 20 P - 80 FL
    elif percentage_parasites == 0.3:
        beta_distribution_parameters = [7, 8.5, 2, 7]      # 30 P - 70 FL
    elif percentage_parasites == 0.4:
        beta_distribution_parameters = [7, 5.5, 2.75, 7]   # 40 P - 60 FL
    elif percentage_parasites == 0.5:
        beta_distribution_parameters = [7, 3.5, 3.5, 7]    # 50 P - 50 FL
    return beta_distribution_parameters

def evaluation(nodelist, fitch_MP_nodelist1, fitch_MP_nodelist2, fitch_MP_nodelist3, fitch_MP_nodelist4):
    result_list = [['id','original tag', 'fitch1', 'fitch2', 'fitch3', 'fitch4']]
    differences = [0, 0, 0, 0]
    number_nodes = 0
    for i in range(0, len(nodelist)):
        real_value = nodelist[i][2]
        # ---------------- Fitch1 ----------------
        f_value = fitch_MP_nodelist1[i][3]
        if f_value == '':
            fitch_MP_nodelist1[i][3] = '-'
        else:
            number_nodes += 1
            if f_value == '0&1':
                f_value = 0.5
            f_value = float(f_value)
            differences[0] += abs(f_value - real_value)
        # ---------------- Fitch2 ----------------
        f_value = fitch_MP_nodelist2[i][3]
        if f_value == '':
            fitch_MP_nodelist2[i][3] = '-'
        else:
            number_nodes += 1
            if f_value == '0&1':
                f_value = 0.5
            f_value = float(f_value)
            differences[1] += abs(f_value - real_value)
        # ---------------- Fitch3 ----------------
        f_value = fitch_MP_nodelist3[i][3]
        if f_value == '':
            fitch_MP_nodelist3[i][3] = '-'
        else:
            number_nodes += 1
            if f_value == '0&1':
                f_value = 0.5
            f_value = float(f_value)
            differences[2] += abs(f_value - real_value)
        # ---------------- Fitch4 ----------------
        f_value = fitch_MP_nodelist4[i][3]
        if f_value == '':
            fitch_MP_nodelist4[i][3] = '-'
        else:
            number_nodes += 1
            if f_value == '0&1':
                f_value = 0.5
            f_value = float(f_value)
            differences[3] += abs(f_value - real_value)
        # --------------------------------
        result_list.append([nodelist[i][0], nodelist[i][2], fitch_MP_nodelist1[i][3], fitch_MP_nodelist2[i][3], fitch_MP_nodelist3[i][3], fitch_MP_nodelist4[i][3]])

    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result_list)
    # pprint(result_list)
    differences[1] = round(differences[1], 2)
    differences[2] = round(differences[2], 2)
    f_dif_p1 = 100 - (differences[0] / number_nodes * 100)
    f_dif_p2 = 100 - (differences[1] / number_nodes * 100)
    f_dif_p3 = 100 - (differences[2] / number_nodes * 100)
    f_dif_p4 = 100 - (differences[3] / number_nodes * 100)
    print(number_nodes)
    diff_percentage = [f_dif_p1, f_dif_p2, f_dif_p3, f_dif_p4]
    return diff_percentage

def metadata():
    leaf_nodes = 2300000        # 2 300 000 Eukaryota
    number_FL = 88967 #FL
    number_P = 43674 #P
    print("real OTL tree: 2 500 000 nodes: 240 000 internal,", leaf_nodes, "leaf nodes")
    print("Information about species from GloBI:", number_P, "#P,", number_FL, "#FL")
    percentage_P = 1 / leaf_nodes * number_P
    percentage_FL = 1 / leaf_nodes * number_FL
    percentage_U = 1 - percentage_P - percentage_FL
    print("=>", round(percentage_P * 100, 2), "% parasites,", round(percentage_FL * 100, 2), "% freeliving =>", round(percentage_U * 100, 2), "% unknown leaf nodes")
    return

main()
