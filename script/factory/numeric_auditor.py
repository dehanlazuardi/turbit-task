from .numeric_audit import numeric_factory

class NumericAuditor:
    def audit(self, data, name: str):
        auditor = numeric_factory.get(name)
        auditor.add_data(data)
        auditor.audit()
        return auditor.get_result()