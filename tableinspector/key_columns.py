import sys
import os
import argparse
import pandas as pd
import numpy as np
import table
import utils

# TODO:
    # Tests
    # Input validity?
    # Print information along the way? How the data has been cleaned, completion percentage etc.

class KeyColumn():
    
    def __init__(self, columns, filename):
        self.columns = columns
        self.filename = filename

    # prints candidates nicely
    def print(self):
        print(f"Candidates for the key column of {self.filename} are: ", end="")
        print(*self.columns, sep=", ")

def check_combination(tbl, combinations_with_values, key_found):
    """ Check if values in every row of a combination of columns is unique.
    """

    candidates = []
    # Check for uniqueness
    for combination in combinations_with_values:    
            if utils.all_unique(combinations_with_values[combination]):
                candidates.append(combination)
                key_found = True

    return candidates, key_found

def find_combination_values(combinations_list, tbl, combination_size):
    """ For each combination of columns, get the values in each row and zip them together.
    """
    combinations_with_values = {}
    # For each combination, zip together the values for each row in the combination
    for combination in combinations_list:
        values = []
        # Getting all the values to be zipped
        for i in range(combination_size):
            if combination_size == 1:
                values.append(combination)
            else:
                values.append(tbl.df[combination[i]])
        combinations_with_values[combination] = list(zip(*values))

    return combinations_with_values

def clean_data(tbl):

    # An empty cell can't be used as a key
    tbl.remove_nan_columns()

    # Even a single duplicate row would result in no key columns.
    tbl.remove_duplicates()

def find_key_column_candidates(tables, verbose=True):
    """ Idea: Check all columns for uniqueness, then check all pairs of columns for uniqueness etc. until key column(s) found.
    """
    
    #Setup
    key_column_candidates = []

    for tbl in tables:

        # Remove duplicate rows and columns that contain empty cells
        clean_data(tbl)

        # Setup
        key_found = False
        combination_size = 1
        number_of_columns = len(tbl.df.columns)

        while not key_found and combination_size <= number_of_columns:
            
            # get a list of all possible combinations
            combinations_list \
                = utils.generate_combinations(tbl.df.columns, combination_size)
            # for those combinations, get the values
            combinations_with_values \
                = find_combination_values(combinations_list, tbl, combination_size)
            # check those combinations of values for uniqueness across all rows
            candidates, key_found \
                = check_combination(tbl, combinations_with_values, key_found)
            
            combination_size = combination_size + 1
    
        key_columns = KeyColumn(candidates, tbl.filename)
        key_column_candidates.append(key_columns)
        if verbose:
            key_columns.print()

    return key_column_candidates

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
    
    find_key_column_candidates(tables)

if __name__ == '__main__':
    main(*sys.argv[1:])