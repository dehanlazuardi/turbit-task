import unittest
import pandas as pd
import numpy as np
from .. import data_clean

class CleanTest(unittest.TestCase):
    def test_PDCleaner(self):
        # prepare data
        df = pd.DataFrame.from_dict({
            "col_1    " : ["unit", "-1", "3", "2.6"],
            "       col_2" : ["", "0", "0", "0"]
        })

        df_answer = pd.DataFrame.from_dict({
            "col_1" : ["-1", "3", "2.6"],
            "col_2" : ["0", "0", "0"],
            "col_1 unit": ["unit", "unit", "unit"]
        })

        # audit data
        cleaner = data_clean.PDCleaner()
        cleaner.add_data(df)
        cleaner.clean()
        res = cleaner.get_result()

        # test result
        self.assertEqual(df_answer.to_dict(), res.to_dict())

