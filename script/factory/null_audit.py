import string
from tokenize import String
import pandas as pd
import numpy as np

class PDNullAuditor:
    def __init__(self):
        self._dataframe = None

    def _remove_white_space(self):
        """
            clear white space. 
            if "" left, will be replace by nan.
            to avoid counted as non null.
        """
        # remove white space
        self._dataframe = self._dataframe.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        # "" to nan, to avoid counted as non null
        self._dataframe = self._dataframe.replace("", np.nan)

    def add_data(self, data):
        self._dataframe = data
    
    def audit(self):
        """
            count number null for each column 
        """
        self._remove_white_space()
        # count nulls
        self._nulls_info = self._dataframe.isnull().sum()


    def get_result(self):
        return self._nulls_info

class NullAuditorFactory:
    def __init__(self):
        self._auditor = {}

    def register(self, name: string, function):
        self._auditor[name] = function

    def get(self, name):
        auditor = self._auditor.get(name)
        if auditor == None:
            raise ValueError(name)
        return auditor()

null_factory = NullAuditorFactory()
null_factory.register('pd_null', PDNullAuditor)