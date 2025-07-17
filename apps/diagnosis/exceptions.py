# apps/diagnosis/exceptions.py
class DiagnosisError(Exception):
    """استثناء أساسي لتطبيق التشخيص."""
    pass

class ModelInferenceError(DiagnosisError):
    """يحدث عند فشل استدلال النموذج."""
    pass