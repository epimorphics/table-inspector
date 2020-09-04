import sys
import key_columns
import os
import argparse
import pandas as pd
import numpy as np
import table
import utils
import unittest

class TestKeyColumns(unittest.TestCase):

    def test_check_combination_for_uniqueness(self):

        current_location = str(os.getcwd())
        test_file_location = current_location + "\\test_data\\test_csv_7.csv"
        
        tbl = table.Table(test_file_location)
        combination_size = 2
        combinations_list = utils.generate_combinations(tbl.df.columns, combination_size)
        combinations_with_values = utils.find_combination_values(combinations_list, tbl, combination_size)

        candidates, key_found = key_columns.check_combination_for_uniqueness(tbl, combinations_with_values, False)
        

        expected_candidates = [('column2', 'column3')]
        self.assertEqual(candidates, expected_candidates)
        self.assertTrue(key_found)


if __name__  == '__main__':
    unittest.main()