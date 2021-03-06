"""Cross validation of leave 100 out results."""

import csv
from pprint import pprint

from numpy import array
from scipy import stats
from termcolor import colored


def main():
    """main"""
    nodelist = []
    cross_evaluation_results = []

    print(colored("---------------- read nodelist ----------------", "green"))
    nodelist_path = './data/nodelist/Eukaryota-castor.csv' 
    #                0    1              2       3       4           5
    # nodelist    - [id, originaltag, finaltag, depth, heights, nr_children]
    with open(nodelist_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader, None)      # skip the header
        for row in reader:
            if row != []:
                ott_id = row[0]
                originaltag = row[1]
                finaltag = float(row[2])
                depth = row[3]
                nr_children = row[5]
                run = []
                new_finaltag = []
                correct_predicted = ""
                nodelist.append([ott_id, originaltag, finaltag, depth, nr_children, run, new_finaltag, correct_predicted])
    print(len(nodelist))

    print(colored("---------------- read leave 100 out nodelists ----------------", "green"))
    for run in range(0, 100):
        print("run:", run)
        index = 0
        changed_tag = 0
        loose_tag = 0
        loose_FL = 0
        loose_P = 0
        distance = 0
        distance_leaf = 0
        distance_inner = 0

        nodelist_path = './data/evaluation/Eukaryota' + str(run) + '-castor.csv' 
        #                0    1              2       3       4           5
        # nodelist    - [id, originaltag, finaltag, depth, heights, nr_children]
        with open(nodelist_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            next(reader, None)      # skip the header
            for row in reader:
                if row != []:
                    ott_id = row[0]
                    originaltag = row[1]
                    finaltag = float(row[2])
                    if index < len(nodelist):
                        if nodelist[index][0] == ott_id:
                            if originaltag != nodelist[index][1]:
                                # ----------------------------------
                                nodelist[index][5].append(run)
                                nodelist[index][6].append(finaltag)
                                if float(nodelist[index][1])-1 == finaltag:
                                    if nodelist[index][7] == 'False':
                                        print('different prediction!')
                                        nodelist[index][7] = 'True$False'
                                    else:
                                        nodelist[index][7] = 'True'
                                else: 
                                    if nodelist[index][7] == 'True':
                                        print('different prediction!')
                                        nodelist[index][7] = 'True$False'
                                    else:
                                        nodelist[index][7] = 'False'
                                # ----------------------------------
                                if originaltag != 'NA':
                                    changed_tag += 1
                                else:
                                    loose_tag += 1
                                    if nodelist[index][1] == '1':
                                        loose_FL += 1
                                    else:
                                        loose_P += 1
                            distance = distance + abs(nodelist[index][2] - finaltag)
                            if nodelist[index][4] == '0':
                                distance_leaf = distance_leaf + abs(nodelist[index][2] - finaltag)
                            else:
                                distance_inner = distance_inner + abs(nodelist[index][2] - finaltag)

                        else:
                            print('Error: the nodelist entry-otts are unequal:')
                            print(nodelist[index][0], '!=', ott_id)
                    index += 1
        cross_evaluation_results.append([run, distance, distance_leaf, distance_inner, changed_tag, loose_tag, loose_FL, loose_P])
    # pprint(cross_evaluation_results)
    
    print(colored("---------------- Save nodelist ----------------", "green"))
    nodelist_path = './data/evaluation/Eukaryota-cross_evaluation.csv' 
    header = ['ott_id', 'originaltag', 'finaltag', 'depth', 'nr_children', 'run', 'new_finaltag', 'correct_predicted']
    with open(nodelist_path, 'w') as nodelist_file:
        writer = csv.writer(nodelist_file, delimiter=',')
        writer.writerow(header)
        for row in nodelist:
            writer.writerow(row)

    print(colored("---------------- cross evaluation stats ----------------", "green"))
    less_FL_results = []
    less_P_results = []
    for element in cross_evaluation_results:
        if element[6] < 54:
            less_FL_results.append(element)
        if element[7] < 39:
            less_P_results.append(element)

    cross_evaluation_results = array(cross_evaluation_results)
    print("distance:")
    print(stats.describe(cross_evaluation_results[:, 1]))
    print("distance_leaf:")
    print(stats.describe(cross_evaluation_results[:, 2]))
    print("distance_inner:")
    print(stats.describe(cross_evaluation_results[:, 3]))
    print("changed_tag:")
    print(stats.describe(cross_evaluation_results[:, 4]))
    print("loose_tag:")
    print(stats.describe(cross_evaluation_results[:, 5]))
    print("loose_FL:")
    print(stats.describe(cross_evaluation_results[:, 6]))
    print("loose_P:")
    print(stats.describe(cross_evaluation_results[:, 7]))

    print('---- less FL and less P ----')

    
    print(len(less_FL_results))
    print(len(less_P_results))
    less_FL_results = array(less_FL_results)
    less_P_results = array(less_P_results)

    print("distance:")
    print(stats.describe(less_FL_results[:, 1]))
    print(stats.describe(less_P_results[:, 1]))
    print("distance_leaf:")
    print(stats.describe(less_FL_results[:, 2]))
    print(stats.describe(less_P_results[:, 2]))
    print("distance_inner:")
    print(stats.describe(less_FL_results[:, 3]))
    print(stats.describe(less_P_results[:, 3]))
    print("changed_tag:")
    print(stats.describe(less_FL_results[:, 4]))
    print(stats.describe(less_P_results[:, 4]))
    print("loose_tag:")
    print(stats.describe(less_FL_results[:, 5]))
    print(stats.describe(less_P_results[:, 5]))
    print("loose_FL:")
    print(stats.describe(less_FL_results[:, 6]))
    print(stats.describe(less_P_results[:, 6]))
    print("loose_P:")
    print(stats.describe(less_FL_results[:, 7]))
    print(stats.describe(less_P_results[:, 7]))

    return

main()
