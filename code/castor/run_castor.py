"""Maximum parsimony algorithm from Sankoff implemented in the R package castor"""
import csv
import datetime
import sys
from code.utilities.castor_util import sankoff_parsimony
from code.utilities.Helpers import print_time

from termcolor import colored

# input arguments
args = sys.argv

# values from  input:
subtree_name = sys.argv[1]

# examples: 'Eukaryota'

# global variables:
START_TIME = datetime.datetime.now().replace(microsecond=0)
CURRENT_TIME = datetime.datetime.now().replace(microsecond=0)

print(colored("------------------------ Sankoff Maximum Parsimony ------------------------", "green"))

def main():
    global START_TIME
    global CURRENT_TIME

    print('Run castor - Sankoff parsimony - for ', subtree_name)

    print(colored("---------------- Sankoff parsimony ----------------", "green"))
    nodelist = sankoff_parsimony(-1)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("---------------- Save nodelist ----------------", "green"))
    nodelist_path = './data/nodelist/' + subtree_name + '-castor.csv' 
    header = ['ott_id', 'originaltag', 'finaltag', 'depth', 'heights', 'nr_children']
    with open(nodelist_path, 'w') as nodelist_file:
        writer = csv.writer(nodelist_file, delimiter=',')
        writer.writerow(header)
        for row in nodelist:
            writer.writerow(row)
    CURRENT_TIME = print_time(CURRENT_TIME)
    print(colored("--------------------------------", "green"))
    return

main()
