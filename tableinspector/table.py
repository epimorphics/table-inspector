import pandas as pd
import os

class Table():

    def __init__(self, location):
        self.location = location
        self.df = pd.read_csv(location)
        self.original_df = self.df.copy()
        self.filename = os.path.basename(location)

    def remove_nan_columns(self):
        """ Removes any columns that contain a nan
        """

        for column in self.df.columns:
            if self.df[column].isna().values.any():
                self.df = self.df.drop(column, axis=1)

    def remove_duplicates(self):
        """ Removes all duplicate rows, keeping the first occurence
        """
        self.df = self.df.drop_duplicates()