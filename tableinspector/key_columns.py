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

def check_combination_for_uniqueness(tbl, combinations_with_values, key_found):
    """ Check if values in every row of a combination of columns is unique.
    """

    candidates = []
    # Check for uniqueness
    for combination in combinations_with_values:
        if utils.all_unique(combinations_with_values[combination]):
            candidates.append(combination)
            key_found = True

    return candidates, key_found

def clean_tables(tbls):
    
    for tbl in tbls:

        # Even a single duplicate row would result in no key columns.
        tbl.remove_duplicates()

        # An empty cell can't be used as a key?
        # tbl.remove_nan_columns()

    return tbls

def find_key_column_candidates(tables, verbose=True):
    """ Idea: Check all columns for uniqueness, then check all pairs of columns for uniqueness etc. until key column(s) found.
    """
    
    #Setup
    key_column_candidates = []

    for tbl in tables:

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
                = utils.find_combination_values(combinations_list, tbl, combination_size)
            # check those combinations of values for uniqueness across all rows
            candidates, key_found \
                = check_combination_for_uniqueness(tbl, combinations_with_values, key_found)
            
            combination_size = combination_size + 1
    
        key_columns = KeyColumn(candidates, tbl.filename)
        key_column_candidates.append(key_columns)
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
    cleaned_tables = clean_tables(tables)
    
    key_column_candidates = find_key_column_candidates(cleaned_tables)

if __name__ == '__main__':
    main(*sys.argv[1:])