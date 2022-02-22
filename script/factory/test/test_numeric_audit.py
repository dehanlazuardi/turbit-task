import unittest
import pandas as pd
import numpy as np
from .. import numeric_audit

class NumericAuditTest(unittest.TestCase):
    def test_PDNumericEditor(self):
        # prepare data
        df = pd.DataFrame.from_dict({
            "col_1" : ["a", "-1", np.nan, "2.6"]
        })
        number_nan = 2

        # audit data
        auditor = numeric_audit.PDNumericAuditor()
        auditor.add_data(df)
        auditor.audit()
        res = auditor.get_result()

        # test result
        self.assertEqual(number_nan, res["col_1"])

