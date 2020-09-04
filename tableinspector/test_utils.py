import utils
import os
import table
from itertools import combinations
from collections import defaultdict
import unittest

class TestUtils(unittest.TestCase):

    def test_generate_tables(self):

        current_location = str(os.getcwd())
        test_files_location = current_location + "\\test_data"

        num_csv_files = 0
        num_files = 0
        for file in os.listdir(test_files_location):
            if file.endswith(".csv"):
                num_csv_files += 1
            num_files += 1

        tables = utils.generate_tables(test_files_location)
        expected_num_csv_files = num_files
        self.assertEqual(len(tables), expected_num_csv_files)

        for tbl in tables:
            self.assertIs(type(tbl), table.Table)

    def test_generate_combinations(self):
        
        tbl = table.Table(str(os.getcwd()) + "\\test_data\\test_csv_3.csv")
        combination_size = 2
        combinations_list = utils.generate_combinations(tbl.df.columns, combination_size)

        self.assertIn(('column1', 'column2'), combinations_list)
        self.assertIn(('column1', 'column3'), combinations_list)
        self.assertIn(('column1', 'column4'), combinations_list)
        self.assertIn(('column2', 'column3'), combinations_list)
        self.assertIn(('column2', 'column4'), combinations_list)
        self.assertIn(('column3', 'column4'), combinations_list)

        tbl = table.Table(str(os.getcwd()) + "\\test_data\\test_csv_4.csv")
        combinations_list = utils.generate_combinations(tbl.df.columns, combination_size)
        
        num_combinations = len(combinations_list)
        expected_num_combinations = 66
        self.assertEqual(num_combinations, expected_num_combinations)

    def test_find_combination_values(self):
        tbl = table.Table(str(os.getcwd()) + "\\test_data\\test_csv_1.csv")
        combination_size = 2
        combinations_list = utils.generate_combinations(tbl.df.columns, combination_size)
        combinations_with_values = utils.find_combination_values(combinations_list, tbl, combination_size)
        
        self.assertIn(('column1', 'column2'), combinations_with_values)
        self.assertIn(('A', 'B'), combinations_with_values[('column1', 'column2')])
        self.assertIn(('D', 'E'), combinations_with_values[('column1', 'column2')])

    def test_all_unique(self):

        unique_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertTrue(utils.all_unique(unique_list))

        non_unique_list = [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertFalse(utils.all_unique(non_unique_list))

    def test_depth_first_search(self):
        pass

    def test_merge_combinations(self):

        test_combinations = [(1, 2), (2, 3), (4, 5), (6, 7), (7, 8), (8, 9)]
        test_merge = utils.merge_combinations(test_combinations)

        expected_size = 3
        self.assertEqual(len(test_merge), expected_size)

        self.assertIn([1, 2, 3], test_merge)
        self.assertIn([4, 5], test_merge)
        self.assertIn([6, 7, 8, 9], test_merge)

if __name__  == '__main__':
    unittest.main()