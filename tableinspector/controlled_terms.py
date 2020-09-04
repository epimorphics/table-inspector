import sys
import os
import argparse
import pandas as pd
import numpy as np
from itertools import combinations
import utils

#TODO:
    # Tests
    # Input validity?

    # Tells you that output are some form of subsets of each other, not what the relationships actually are.

class ControlledTerms():
    def __init__(self, combination):
        self.combination = combination

    def print(self):
        for column in self.combination:
            column.print()
        print()

class Column():
    def __init__(self, table, column):
        self.table = table
        self.column = column
        self.unique_values = table.df[column].unique()

    def print(self):
        print(f"Table: {self.table.filename}, Column: {self.column}")

def print_controlled_terms(controlled_terms):
    for terms in controlled_terms:
        terms.print()

def check_combination(combination):
    if set(combination[0].unique_values).issubset(set(combination[1].unique_values)) or set(combination[1].unique_values).issubset(set(combination[0].unique_values)):
        return True
    return False

def generate_columns(tables):
    """
    """

    columns = []
    for table in tables:
        for column in table.df.columns:
            column = Column(table, column)
            columns.append(column)

    return columns

def find_controlled_terms(tables):
    
    # Setup
    controlled_terms = []
    candidate_controlled_terms = []
    columns = generate_columns(tables)

    #temporary
    max_combination_length = 2
    combinations_list = utils.generate_combinations(columns, max_combination_length)

    for combination in combinations_list:
        if check_combination(combination):
                candidate_controlled_terms.append(combination)

    merged_combinations = list(utils.merge_combinations(candidate_controlled_terms))

    for merged_combination in merged_combinations:
        controlled_term = ControlledTerms(merged_combination)
        controlled_terms.append(controlled_term)
        controlled_term.print()

    return controlled_terms

def clean_tables(tables):
    pass

def parse_arguments(*args):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", dest="location", help="specify file to process")
    group.add_argument("-d", "--directory", dest="location", help="specify directory to process")
    args = parser.parse_args()

    return args.location

def main(*args):
    destination = parse_arguments(*args)
    tables = utils.generate_tables(destination)

    controlled_terms = find_controlled_terms(tables)

if __name__ == '__main__':
    main(*sys.argv[1:])