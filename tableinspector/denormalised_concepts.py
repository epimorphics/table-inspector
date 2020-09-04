import sys
import os
import argparse
import pandas as pd
import numpy as np
from itertools import combinations
import utils
from collections import defaultdict

"""TODO:
    # Tests
    # Input validity?
    # Arguments for how to clean data? Getting rid of single valued columns, unique columns, empty columns?
    # Threshold? What percentage are the  same? >50?
    # Speed up by stopping early when checking a combination?

    # At the moment, the code checks for Case 1:

    Case 1:
          A       B
          A       B
          A       B
          D       E
          D       E

    Output (COL1, (COL2)) (COL2, (COL1))   ((COL1, COL2), ())

    Case 2:
          A       B
          A       B
          A       B
          A       C
          A       C
          A       C
          A       C
    
    Output: (COL2, (COL1)) 

    # Case 3:
          A       B       D       F
          A       B       D       F
          A       B       D       F
          A       C       D       G
          A       C       D       G
          A       C       E       G
          A       C       E       G

    Output: (COL2, (COL1, COL4)), (COL3, (COL1)), (COL4, (COL1, COL2))  ((COL2, COL4), (COL1)), (COL3, (COL1))
"""


class DenormalisedConcept():
    
    def __init__(self, columns, filename):
        self.columns = columns
        self.filename = filename

    def print(self):
        print(f"Denormalised concepts found in {self.filename}: ", end="")
        print(*self.columns, sep=", ")

def check_combination(combination_with_values):
    """
    """

    corresponding_values = defaultdict(set)

    for first, second in combination_with_values:
        corresponding_values[first].add(second)
        corresponding_values[second].add(first)
    
    if all(len(corresponding_values[key]) == 1 for key in corresponding_values):
        return True
    else:
        return False

def clean_tables(tbls):

    for tbl in tbls:

        #tbl.remove_nan_columns()

        #tbl.remove_unique_columns()

        #tbl.remove_single_value_columns()

        pass

    return tbls

def find_denormalised_concepts(tbls):

    # Setup
    denormalised_concepts = []

    for tbl in tbls:

        # Setup
        combination_size = 2
        candidate_denormalised_concepts = []

        # get a list of all possible combinations
        combinations_list \
            = utils.generate_combinations(tbl.df.columns, combination_size)
        # for those combinations, get the values
        combinations_with_values \
            = utils.find_combination_values(combinations_list, tbl, combination_size)
        
        for combination in combinations_list:

            if check_combination(combinations_with_values[combination]):
                candidate_denormalised_concepts.append(combination)
        
        merged_combinations = utils.merge_combinations(candidate_denormalised_concepts)

        denormalised_concept = DenormalisedConcept(list(merged_combinations), tbl.filename)
        denormalised_concepts.append(denormalised_concept)
        denormalised_concept.print()

    return denormalised_concepts

def parse_arguments(*args):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", dest="location", help="specify file to process")
    group.add_argument("-d", "--directory", dest="location", help="specify directory to process")
    args = parser.parse_args()

    return args.location

def main(*args):

    # location of csv files to process
    location = parse_arguments(*args)
    tables = utils.generate_tables(location)
    cleaned_tables = clean_tables(tables)

    denormalised_concepts = find_denormalised_concepts(cleaned_tables)

if __name__ == '__main__':
    main(*sys.argv[1:])