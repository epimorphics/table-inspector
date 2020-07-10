import sys
import os
import argparse
import pandas as pd
import numpy as np
from itertools import combinations
import table

# TODO:
    # Input Validity?

class TableKeyColumns():
    
    def __init__(self, columns, filename):
        self.columns = columns
        self.filename = filename

    def print(self):
        print("Candidates for the key column of " + self.filename + " are:")
        print(self.columns)


def print_key_columns(key_columns_all_tables):
    for key_columns_specific_table in key_columns_all_tables:
        key_columns_specific_table.print()

def all_unique(values):
    s = set()
    return not any(i in s or s.add(i) for i in values)

def find_key_column_candidates(tbl, combinations_with_values, key_found):
    key_column_candidates = []
    # Check for uniqueness
    for combination in combinations_with_values:
            if all_unique(combinations_with_values[combination]):
                key_column_candidates.append(combination)
                key_found = True

    return key_column_candidates, key_found

def find_combination_values(combinations_list, tbl, combination_size):
    combinations_with_values = {}
    # For each combination, zip together the values for each row in the combination
    for combination in combinations_list:
        values = []
        # Getting all the values to be zipped
        for i in range(combination_size):
            values.append(tbl.df[combination[i]])
        combinations_with_values[combination] = list(zip(*values))

    return combinations_with_values

def generate_combinations(tbl, combination_size):
    # Generate list of column combinations of size combination_size
    combinations_list = list(combinations(tbl.df.columns, combination_size))

    return combinations_list

def clean_data(tbl):
    tbl.remove_columns_containing_empty_cells()
    tbl.remove_duplicates()

# Idea: Check all columns for uniqueness, then check all pairs of columns for uniqueness etc. until key column(s) found.
def find_key_columns_specific_table(tbl):

    # Remove columns that contain empty cells, and duplicate rows
    clean_data(tbl)

    # Setup
    key_found = False
    combination_size = 2
    number_of_columns = len(tbl.df.columns)

    while not key_found and combination_size <= number_of_columns:

        combinations_list \
            = generate_combinations(tbl, combination_size)
        combinations_with_values \
            = find_combination_values(combinations_list, tbl, combination_size)
        key_column_candidates, key_found \
            = find_key_column_candidates(tbl, combinations_with_values, key_found)

        combination_size = combination_size + 1

    return key_column_candidates

def find_key_columns_all_tables(tables):
    
    #Setup
    key_columns_all_tables = []

    for tbl in tables:
        key_column_candidates = find_key_columns_specific_table(tbl)
        key_columns_all_tables.append(TableKeyColumns(key_column_candidates, tbl.filename))

    return key_columns_all_tables

def generate_tables(location):
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

def parse_arguments(*args):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", dest="location", help="specify file to process")
    group.add_argument("-d", "--directory", dest="location", help="specify directory to process")
    args = parser.parse_args()

    return args.location

def main(*args):
    location = parse_arguments(*args)
    tables = generate_tables(location)
    key_columns_all_tables = find_key_columns_all_tables(tables)
    
    print_key_columns(key_columns_all_tables)

if __name__ == '__main__':
    main(*sys.argv[1:])