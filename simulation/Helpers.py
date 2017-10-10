"""some simple helper functions"""

def find_element_in_nodelist(id_name, nodelist):
    """finds id in nodelist and returns the element"""
    for element in nodelist:
        if id_name == element[0]:
            return element
    print('error: element does not exist in nodelist')
