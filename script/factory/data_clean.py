import pandas as pd
import numpy as np

class PDCleaner:
    def __init__(self):
        self._dataframe = None

    def add_data(self, data):
        self._dataframe = data
    
    def clean(self):
        # strip white space from column names
        self._dataframe.columns = self._dataframe.columns.str.strip()

        # extract unit from first row, make new unit columns
        units = self._dataframe.iloc[0]
        units = units.str.strip()
        units = units.replace("", np.nan)
        units = units.dropna()
        for col in list(self._dataframe.columns):
            if col in list(units.index):
                # create column, assign unit to the new columns
                col_unit_name = col+" unit"
                self._dataframe[col_unit_name] = units[col]

        # restart indexed to 0 because we already drop the first index
        self._dataframe = self._dataframe.drop([0]).reset_index(drop=True)
        
    def get_result(self):
        return self._dataframe

class CleanerFactory:
    def __init__(self):
        self._cleaner = {}

    def register(self, name: str, function):
        self._cleaner[name] = function

    def get(self, name: str):
        cleaner = self._cleaner.get(name)
        if cleaner == None:
            raise ValueError(name)
        return cleaner()

cleaner_factory = CleanerFactory()
cleaner_factory.register('pd_cleaner', PDCleaner)