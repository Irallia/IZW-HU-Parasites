"""some simple helper functions"""

def find_element_in_nodelist(id_name, nodelist):
    """finds id in nodelist and returns the element"""
    return nodelist[int(id_name.split("$")[1])]
