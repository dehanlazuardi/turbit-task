import pandas as pd

class PDNumericAuditor:
    def __init__(self):
        self._data = None

    def _is_digit(self, column_data):
        column_data = column_data.astype(str).str.replace(".", "", 1, regex=False).str.lstrip('-')
        column_data = column_data.str.isdigit()
        return column_data

    def _count_non_numeric(self, column_data):
        non_numeric = 0
        if False in set(column_data):
            non_numeric = column_data.value_counts()[False]
        
        return non_numeric

    def add_data(self, data):
        self._data = data

    def audit(self):
        self._non_numeric_info = {}
        column_names = list(self._data.columns)
        for col_name in column_names:
            digit_series = self._is_digit(self._data[col_name])
            non_numeric = self._count_non_numeric(digit_series)
            self._non_numeric_info[col_name] = non_numeric

    def get_result(self):
        return pd.Series(data = self._non_numeric_info, index = self._non_numeric_info.keys())


class NumericAuditorFactory:
    def __init__(self):
        self._auditor = {}

    def register(self, name: str, function):
        self._auditor[name] = function

    def get(self, name: str):
        auditor = self._auditor.get(name)
        if auditor == None:
            raise ValueError(name)
        return auditor()

numeric_auditor_factory = NumericAuditorFactory()
numeric_auditor_factory.register('pd_numeric', PDNumericAuditor)
