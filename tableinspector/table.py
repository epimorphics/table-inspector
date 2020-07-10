import pandas as pd
import os

class Table():

    def __init__(self, location):
        self.location = location
        self.df = pd.read_csv(location)
        self.original_df = self.df.copy()
        self.filename = os.path.basename(location)

    # Removes any columns that contain an empty cell
    def remove_columns_containing_empty_cells(self):
        for column in self.df.columns:
            if self.df[column].isna().values.any():
                self.df = self.df.drop(column, axis=1)

    # Removes all duplicate rows, keeping the first occurence
    def remove_duplicates(self):
        self.df = self.df.drop_duplicates()