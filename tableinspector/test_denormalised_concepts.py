import denormalised_concepts
import sys
import os
import argparse
import pandas as pd
import numpy as np
from itertools import combinations
import utils
from collections import defaultdict
import table
import unittest

class TestDenormalisedConcepts(unittest.TestCase):

    def test_check_combination(self):
        current_location = str(os.getcwd())
        test_file_location = current_location + "\\test_data\\test_csv_8.csv"
        
        tbl = table.Table(test_file_location)
        combination_size = 2
        combinations_list = utils.generate_combinations(tbl.df.columns, combination_size)
        combinations_with_values = utils.find_combination_values(combinations_list, tbl, combination_size)

        test_combination = ('column1', 'column2')
        self.assertTrue(denormalised_concepts.check_combination(combinations_with_values[test_combination]))
        test_combination = ('column2', 'column3')
        self.assertTrue(denormalised_concepts.check_combination(combinations_with_values[test_combination]))
        test_combination = ('column1', 'column3')
        self.assertTrue(denormalised_concepts.check_combination(combinations_with_values[test_combination]))

if __name__  == '__main__':
    unittest.main()
