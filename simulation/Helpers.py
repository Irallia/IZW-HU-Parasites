def find_element_in_nodelist(id, nodelist):
    for element in nodelist:
        if id == element[0]:
            return element
    print('error: element does not exist in nodelist')