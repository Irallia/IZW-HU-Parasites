from copy import deepcopy

from utilities import Helpers

def my_parsimony(tree_clade, nodelist):
    """mean based parsimony"""
    # down:
    parsimony_down(tree_clade, nodelist)
    # up:
    parent = Helpers.find_element_in_nodelist(tree_clade.name, nodelist)
    children = []
    for clade in tree_clade.clades:
        child = Helpers.find_element_in_nodelist(clade.name, nodelist)
        children.append(child)
    for i in range(0, len(tree_clade.clades)):
        clade = tree_clade.clades[i]
        child = Helpers.find_element_in_nodelist(clade.name, nodelist)
        sublist = deepcopy(children)
        del sublist[i]
        parsimony_up(clade, nodelist, parent, sublist)
    # final:
    parsimony_final(tree_clade, nodelist)
    return

def parsimony_down(subtree, nodelist):
    """parsimony part: down direction -> from leafs to root"""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    mean = 0
    for clade in subtree.clades:
        child = Helpers.find_element_in_nodelist(clade.name, nodelist)
        # if child is not tagged, first tag it:
        if child[4] == []:
            parsimony_down(clade, nodelist)
        # if child is leaf node:
        if clade.is_terminal():
            if child[4][0][0] == 'FL':
                child[4][0] = 1
            else:
                if child[4][0][0] == 'P':
                    child[4][0] = 0
        mean = mean + child[4][0]     # else: +0 for 'P'
    element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
    # calculate and add mean
    mean = mean / len(subtree.clades)
    element[4].append(mean)
    return

def parsimony_up(subtree, nodelist, parent, siblings):
    """parsimony part: up direction -> from root to leafs"""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    #   parent      - nodelist element
    #   siblings     - [nodelist element]
    if not subtree.is_terminal():

        parent_tag = parent[4]  # parent[4] could look like [['FL', 'P'], ['P']] or [['P']]
        siblings_tags = []
        siblings_tags += parent_tag
        for sibling in siblings:
            siblings_tags += sibling[4]

        element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
        # calculate and add mean
        mean = sum(siblings_tags) / len(siblings_tags)
        element[4].append(mean)

        # go on with children
        children = []
        for clade in subtree.clades:
            child = Helpers.find_element_in_nodelist(clade.name, nodelist)
            children.append(child)
        for i in range(0, len(subtree.clades) - 1):
            clade = subtree.clades[i]
            child = Helpers.find_element_in_nodelist(clade.name, nodelist)
            sublist = deepcopy(children)
            del sublist[i]
            parsimony_up(clade, nodelist, element, sublist)
    return

def parsimony_final(subtree, nodelist):
    """parsimony final part: combine multiple tags of node to one final tag"""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
    # calculate mean
    mean = sum(element[4]) / len(element[4])
    element[2] = str(round(mean,2))

    # go on with children
    if not subtree.is_terminal():
        parsimony_final(subtree.clades[0], nodelist)
        parsimony_final(subtree.clades[1], nodelist)
    return
