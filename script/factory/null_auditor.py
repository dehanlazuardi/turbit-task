from .null_audit import null_factory

class NullAuditor:
    def audit(self, data, name):
        auditor = null_factory.get(name)
        auditor.add_data(data)
        auditor.audit()
        return auditor.get_result()
