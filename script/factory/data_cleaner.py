from .data_clean import cleaner_factory

class NumericAuditor:
    def audit(self, data, name: str):
        auditor = cleaner_factory.get(name)
        auditor.add_data(data)
        auditor.audit()
        return auditor.get_result()