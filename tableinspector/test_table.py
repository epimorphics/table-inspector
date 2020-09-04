import table
import os
import pandas as pd
import unittest


class TestTable(unittest.TestCase):

    def test_remove_nan_columns(self):
        current_location = str(os.getcwd())
        test_file_location = current_location + "\\test_data\\test_csv_5.csv"

        tbl = table.Table(test_file_location)
        initial_columns = list(tbl.df.columns)
        
        tbl.remove_nan_columns()
        initial_columns.remove('column4')
        self.assertEqual(list(tbl.df.columns), initial_columns)

    def test_remove_duplicates(self):
        current_location = str(os.getcwd())
        test_file_location = current_location + "\\test_data\\test_csv_6.csv"

        tbl = table.Table(test_file_location)
        initial_rows = tbl.df.values.tolist()
        expected_rows = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I'], ['J', 'K', 'L'], ['M', 'N', 'O'], ['P', 'Q', 'R']]
        tbl.remove_duplicates()
        rows = tbl.df.values.tolist()
        self.assertEqual(rows, expected_rows)

    def test_remove_unique_columns(self):
        current_location = str(os.getcwd())
        test_file_location = current_location + "\\test_data\\test_csv_5.csv"

        tbl = table.Table(test_file_location)
        initial_columns = list(tbl.df.columns)
        
        tbl.remove_unique_columns()
        initial_columns.remove('column1')
        self.assertEqual(list(tbl.df.columns), initial_columns)

    def test_remove_single_value_columns(self):
        current_location = str(os.getcwd())
        test_file_location = current_location + "\\test_data\\test_csv_5.csv"

        tbl = table.Table(test_file_location)
        initial_columns = list(tbl.df.columns)
        
        tbl.remove_single_value_columns()
        initial_columns.remove('column2')
        initial_columns.remove('column4')
        self.assertEqual(list(tbl.df.columns), initial_columns)

if __name__  == '__main__':
    unittest.main()