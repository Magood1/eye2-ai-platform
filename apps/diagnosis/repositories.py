# apps/diagnosis/repositories.py
from .models import Diagnosis

class DiagnosisRepository:
    """يعزل منطق استعلام قاعدة البيانات للتشخيص."""
    def update_with_success(self, diagnosis_id, result_data):
        Diagnosis.objects.filter(id=diagnosis_id).update(
            status=Diagnosis.Status.SUCCESS,
            result=result_data
        )

    def update_with_failure(self, diagnosis_id, error_message):
        Diagnosis.objects.filter(id=diagnosis_id).update(
            status=Diagnosis.Status.FAILURE,
            error_message=error_message
        )