from Bio import Phylo
from pprint import pprint

def main():
    """main method"""
    # tree = Phylo.read('../../data/opentree9.1_tree/grafted_solution/grafted_solution.tre', 'newick')
    tree = Phylo.read('../../data/opentree9.1_tree/labelled_supertree/labelled_supertree.tre', 'newick')
    # print(tree)
    result = get_metadata(tree.clade, [], [0,0])
    nodelist = result[0]
    depth = result[1]
    metadata = result[2]
    print("root node: ", nodelist[0][0])
    print("mean depth, max depth, min depth:")
    pprint(nodelist[0])
    print(metadata[0] + metadata[1], " nodes")
    print("#internal nodes, #leaf nodes:")
    pprint(metadata)

    return


def get_metadata(subtree, nodelist, metadata):
    """calculate depths of every node"""
    #                   0       1
    #   nodelist    - [ottId, mean depth, max depth, min depth]
    #   metadata    - [#internal nodes, #leaf nodes]
    mean_depth = -1
    max_depth = -1
    min_depth = 10000000000000000000000000
    nodelist.append([subtree.name, mean_depth, max_depth, min_depth])
    current_list_index = len(nodelist) - 1
    # if leaf node, then depth = 1
    if subtree.is_terminal():
        mean_depth = 1
        max_depth = 1
        min_depth = 1
        metadata[1] += 1
    else:
        child_depth = 0
        metadata[0] += 1
        for clade in subtree.clades:
            result = get_metadata(clade, nodelist, metadata)
            nodelist = result[0]
            child_depth = child_depth + result[1][0]
            metadata = result[2]
            if result[1][1] > max_depth:
                max_depth = result[1][1]
            if result[1][2] < min_depth:
                min_depth = result[1][2]
        mean_depth = child_depth/len(subtree.clades) + 1
        max_depth += 1
        min_depth += 1
    nodelist[current_list_index][1] = mean_depth
    nodelist[current_list_index][2] = max_depth
    nodelist[current_list_index][3] = min_depth
    depths = [mean_depth, max_depth, min_depth]
    return [nodelist, depths, metadata]

main()
