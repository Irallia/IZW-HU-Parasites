import sys
from code.evaluation.build_nodelist import build_nodelist
from code.evaluation.run_castor import run_castor

# input arguments
args = sys.argv

# values for simulation:
index = sys.argv[1]
border = int(sys.argv[2])

def main():
    build_nodelist(index, border)
    run_castor(index, border)
    return

main()
