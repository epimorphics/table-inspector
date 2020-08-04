
import os
import table
from itertools import combinations

def generate_tables(location):
    """ Generate tables from csv files.
    """

    # if the destination points to a single csv file
    if location.endswith(".csv"):
        tables = [table.Table(location)]
    # otherwise it's a directory
    else:
        tables = []
        for file in os.listdir(location):
            if file.endswith(".csv"):
                tables.append(table.Table(os.path.join(location , file)))
    
    return tables

def generate_combinations(columns, combination_size):
    """ Generate list of column combinations of size combination_size
    """

    if combination_size == 1:
        combinations_list = columns.tolist()
    else:
        combinations_list = list(combinations(columns, combination_size))

    return combinations_list

def all_unique(values):
    s = set()
    return not any(i in s or s.add(i) for i in values)