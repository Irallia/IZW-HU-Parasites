from copy import deepcopy

from code.utilities.Helpers import find_element_in_nodelist, get_intersect_or_union

# Version 1:
# use only first tag of parent, and every sibling
# get_intersect_or_union(siblings_tags)
# get_intersect_or_union(both)

# Version 2:
# use only first tag of parent, and every sibling
# get_intersect_or_union(both)

# Version 3:
# use every tag
# get_intersect_or_union(siblings_tags)
# get_intersect_or_union(parent_tags)
# get_intersect_or_union(both)

# Version 4:
# use every tag
# get_intersect_or_union(both)

# ----------------------------------------------------------------------------------------
# 100  trees simulated with 10000 leafnodes 40.0 % parasites and 90.0 % unknown leafnodes.
# correctly predicted (including already known leaf nodes):
# differences Fitch1 / Fitch2 / Fitch3 / Fitch4
# | 89.67 % | 89.67 % | 90.72 % |90.74 % |

def parsimony_up(subtree, nodelist, parent, siblings, version):
    if version == 1:
        parsimony_up1(subtree, nodelist, parent, siblings)
    elif version == 2:
        parsimony_up2(subtree, nodelist, parent, siblings)
    elif version == 3:
        parsimony_up3(subtree, nodelist, parent, siblings)
    elif version == 4:
        parsimony_up4(subtree, nodelist, parent, siblings)
    else:
        print("This version number (", version, ") do not exist!")
    return

# -------------------- Version 1 --------------------
def parsimony_up1(subtree, nodelist, parent, siblings):
    """parsimony part: up direction -> from root to leafs"""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    #   parent      - nodelist element
    #   siblings     - [nodelist element]
    element = find_element_in_nodelist(subtree.name, nodelist)

    parent_tag = parent[4][0]  # parent[4] could look like [['0', '1'], ['1']] or [['1']]
    siblings_tags = []
    for sibling in siblings:
        siblings_tags.append(sibling[4][0])

    # get intersection or union
    both_tags = get_intersect_or_union(siblings_tags)
    both_tags = [both_tags]
    both_tags.append(parent_tag)
    tag_list = get_intersect_or_union(both_tags)
    # add new tag
    element[4].append(tag_list)

    # go on with children
    if not subtree.is_terminal():
        children = []
        for clade in subtree.clades:
            child = find_element_in_nodelist(clade.name, nodelist)
            children.append(child)
        for i in range(0, len(subtree.clades)):
            clade = subtree.clades[i]
            child = find_element_in_nodelist(clade.name, nodelist)
            sublist = deepcopy(children)
            del sublist[i]
            parsimony_up1(clade, nodelist, element, sublist)
    return

# -------------------- Version 2 --------------------
def parsimony_up2(subtree, nodelist, parent, siblings):
    """parsimony part: up direction -> from root to leafs"""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    #   parent      - nodelist element
    #   siblings     - [nodelist element]
    element = find_element_in_nodelist(subtree.name, nodelist)

    parent_tag = parent[4][0]  # parent[4] could look like [['0', '1'], ['1']] or [['1']]
    both_tags = []
    both_tags.append(parent_tag)
    for sibling in siblings:
        both_tags.append(sibling[4][0])

    # get intersection or union
    tag_list = get_intersect_or_union(both_tags)
    # add new tag
    element[4].append(tag_list)

    # go on with children
    if not subtree.is_terminal():
        children = []
        for clade in subtree.clades:
            child = find_element_in_nodelist(clade.name, nodelist)
            children.append(child)
        for i in range(0, len(subtree.clades)):
            clade = subtree.clades[i]
            child = find_element_in_nodelist(clade.name, nodelist)
            sublist = deepcopy(children)
            del sublist[i]
            parsimony_up2(clade, nodelist, element, sublist)
    return

# -------------------- Version 3 --------------------
def parsimony_up3(subtree, nodelist, parent, siblings):
    """parsimony part: up direction -> from root to leafs"""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    #   parent      - nodelist element
    #   siblings     - [nodelist element]
    element = find_element_in_nodelist(subtree.name, nodelist)

    parent_tags = parent[4]  # parent[4] could look like [['0', '1'], ['1']] or [['1']]
    siblings_tags = []
    for sibling in siblings:
        siblings_tags += sibling[4]

    # get intersection or union
    both_tags = []
    both_tags.append(get_intersect_or_union(siblings_tags))
    both_tags.append(get_intersect_or_union(parent_tags))
    tag_list = get_intersect_or_union(both_tags)
    # add new tag
    element[4].append(tag_list)

    # go on with children
    if not subtree.is_terminal():
        children = []
        for clade in subtree.clades:
            child = find_element_in_nodelist(clade.name, nodelist)
            children.append(child)
        for i in range(0, len(subtree.clades)):
            clade = subtree.clades[i]
            child = find_element_in_nodelist(clade.name, nodelist)
            sublist = deepcopy(children)
            del sublist[i]
            parsimony_up3(clade, nodelist, element, sublist)
    return

# -------------------- Version 4 --------------------
def parsimony_up4(subtree, nodelist, parent, siblings):
    """parsimony part: up direction -> from root to leafs"""
    # Arguments:
    #   subtree
    #                   0   1       2           3           4
    #   nodelist    - [id, depth, originaltag, finaltag, calc[taglist]]
    #   parent      - nodelist element
    #   siblings     - [nodelist element]
    element = find_element_in_nodelist(subtree.name, nodelist)

    parent_tag = parent[4]  # parent[4] could look like [['0', '1'], ['1']] or [['1']]
    both_tags = []
    both_tags += parent_tag
    for sibling in siblings:
        both_tags += sibling[4]
    
    # get intersection or union
    tag_list = get_intersect_or_union(both_tags)
    # add new tag
    element[4].append(tag_list)

    # go on with children
    if not subtree.is_terminal():
        children = []
        for clade in subtree.clades:
            child = find_element_in_nodelist(clade.name, nodelist)
            children.append(child)
        for i in range(0, len(subtree.clades)):
            clade = subtree.clades[i]
            child = find_element_in_nodelist(clade.name, nodelist)
            sublist = deepcopy(children)
            del sublist[i]
            parsimony_up4(clade, nodelist, element, sublist)
    return
