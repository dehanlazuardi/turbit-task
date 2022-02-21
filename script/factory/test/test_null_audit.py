import unittest
import pandas as pd
import numpy as np
from .. import null_audit

class NullAuditTest(unittest.TestCase):
    def test_PDNullEditor(self):
        # prepare data
        df = pd.DataFrame.from_dict({
            "col_1" : ["a", "     ", np.nan]
        })
        number_nan = 2

        # audit data
        auditor = null_audit.PDNullAuditor()
        auditor.add_data(df)
        auditor.audit()
        res = auditor.get_result()

        # test result
        self.assertEqual(number_nan, res["col_1"])

