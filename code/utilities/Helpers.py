"""some simple helper functions"""

import datetime

from termcolor import colored

# TAGS = ["FL", "P"]
TAGS = [0, 1]

def find_element_in_nodelist(id_name, nodelist):
    """finds id in nodelist and returns the element"""
    element = nodelist[int(id_name.split("$")[1])]
    if element[0] != id_name.split("$")[1]:
        print(id_name, "!=", element)
    return element

def print_time(time_old):
    time_new = datetime.datetime.now().replace(microsecond=0)
    # Text colors: grey, red, green, yellow, blue, magenta, cyan, white
    print(colored("time needed:", "magenta"), time_new - time_old)
    return time_new

def get_intersect_or_union(tags_list):
    """returns the intersection of all list elements, if not empty"""
    # Arguments:
    #   tags_list - a list of tag_lists
    #       tags_list[tag_list]
    if len(tags_list) == 1:
        return tags_list[0]
    # pairwise intersection
    tag_set = []
    while len(tags_list) > 1:
        tag_list_i = tags_list[0]
        tag_list_j = tags_list[1]
        # RULE 1: share any states in common -> assign shared states
        # intersection:
        tag_set = (set(tag_list_i) & set(tag_list_j))
        # RULE 2: no shared states -> assign union of states
        if tag_set == set():
            # union:
            return TAGS
        else:
            tags_list.remove(tag_list_i) # same as 
            tags_list.remove(tag_list_j)
            tags_list.append(list(tag_set))
    return list(tag_set)
