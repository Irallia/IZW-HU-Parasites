from copy import deepcopy
from pprint import pprint

import Helpers

def parsimony(tree_clade, nodelist):
    """parsimony implemented from [COO98] - changed for multifurcating trees"""
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
    # ToDo: final step...
    # parsimony_final(tree_clade, nodelist)
    return

def parsimony_down(subtree, nodelist):
    """parsimony part: down direction -> from leafs to root"""
    # Arguments:
    #   subtree
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    child_tags = []
    for clade in subtree.clades:
        child = Helpers.find_element_in_nodelist(clade.name, nodelist)
        # if child is not tagged, first tag it:
        if child[4] == []:
            parsimony_down(clade, nodelist)
        child_tags.append(child[4][0])

    element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
    # pairwise intersection
    while len(child_tags) > 1:
        tag_list_i = child_tags[0]
        tag_list_j = child_tags[1]
        # RULE 1: share any states in common -> assign shared states
        # intersection:
        tag_set = (set(tag_list_i) & set(tag_list_j))
        # RULE 2: no shared states -> assign union of states
        if tag_set == set():
            # union:
            tag_set = (set().union(['FL'],['P']))
            child_tags = [list(tag_set)]
            # -> stop
        else:
            child_tags.remove(tag_list_i) # same as 
            child_tags.remove(tag_list_j)
            child_tags.append(list(tag_set))
    # add new tag
    element[4].append(list(tag_set))
    return

def parsimony_up(subtree, nodelist, parent, siblings):
    """parsimony part: up direction -> from root to leafs"""
    # Arguments:
    #   subtree
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    #   parent      - nodelist element
    #   siblings     - [nodelist element]
    if not subtree.is_terminal():
        parent_tag = parent[4]  # parent[4] could look like [['FL', 'P'], ['P']] or [['P']]
        siblings_tags = []
        for sibling in siblings:
            siblings_tags.append(sibling[4])

        element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
        # RULE 1: share any states in common -> assign shared states
        # ToDo: intersection, of all pairwise, or only with parent????
        # RULE 2: no shared states -> assign union of states
        # ToDo: union....

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
    #   nodelist      - [id, originaltag, finaltag, calc[taglist]]
    element = Helpers.find_element_in_nodelist(subtree.name, nodelist)
    if not subtree.is_terminal():
        tags = element[3]
        if len(tags) > 1:
            if ('FL&P') in tags[0]:
                element[2] = tags[1]
            else:
                element[2] = tags[0]
            # shared = False
            # # RULE 1: share any states in common -> assign shared states
            # if ('FL' in tags[0]) and ('FL' in tags[1]):
            #     element[2] = 'FL'
            #     # subtree._set_color('blue')
            #     shared = True
            # if ('P' in tags[0]) and ('P' in tags[1]):
            #     if shared:
            #         element[2] = 'FL&P'
            #         # subtree._set_color('magenta')
            #     else:
            #         element[2] = 'P'
            #         # subtree._set_color('red')
            #     shared = True
            # # RULE 2: no shared states -> assign union of states
            # if not shared:
            #     element[2] = 'FL&P'
            #     # subtree._set_color('magenta')
    else:
        element[2] = element[3][0]
    # go on with children
    if not subtree.is_terminal():
        parsimony_final(subtree.clades[0], nodelist)
        parsimony_final(subtree.clades[1], nodelist)
    return
