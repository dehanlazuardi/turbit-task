from .null_audit import null_auditor_factory

class NullAuditor:
    def audit(self, data, name: str):
        auditor = null_auditor_factory.get(name)
        auditor.add_data(data)
        auditor.audit()
        return auditor.get_result()
