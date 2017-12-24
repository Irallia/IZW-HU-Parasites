"""some simple helper functions"""

import datetime

from termcolor import colored


def find_element_in_nodelist(id_name, nodelist):
    """finds id in nodelist and returns the element"""
    return nodelist[int(id_name.split("$")[1])]

def print_time(time_old):
    time_new = datetime.datetime.now().replace(microsecond=0)
    # Text colors: grey, red, green, yellow, blue, magenta, cyan, white
    print(colored("time needed:", "magenta"), time_new - time_old)
    return time_new
