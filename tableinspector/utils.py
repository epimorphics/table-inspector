import os
import table
from itertools import combinations
from collections import defaultdict

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

def find_combination_values(combinations_list, tbl, combination_size):
    """ For each combination of columns, get the values in each row and zip them together.
    """
    combinations_with_values = {}
    # For each combination, zip together the values for each row in the combination
    for combination in combinations_list:
        values = []
        # Getting all the values to be zipped
        if combination_size == 1:
            combinations_with_values[combination] = tbl.df[combination]
        else:
            for i in range(combination_size):
                if combination_size == 1:
                    values.append(combination)
                else:
                    values.append(tbl.df[combination[i]])
            else:
                combinations_with_values[combination] = list(zip(*values))

    return combinations_with_values

def all_unique(values):
    s = set()
    return not any(i in s or s.add(i) for i in values)

def depth_first_search(adjacency_list, vertex, key, visited, result):
    visited.add(vertex)
    result[key].append(vertex)
    for neighbour in adjacency_list[vertex]:
        if neighbour not in visited:
            depth_first_search(adjacency_list, neighbour, key, visited, result)

def merge_combinations(combinations):
    """ Merge combination tuples through common elements
    """

    adjacency_list = defaultdict(list)

    for x, y in combinations:
        adjacency_list[x].append(y)
        adjacency_list[y].append(x)

    result = defaultdict(list)
    visited = set()
    for vertex in adjacency_list:
        if vertex not in visited:
            key = vertex
            depth_first_search(adjacency_list, vertex, key, visited, result)

    return result.values()