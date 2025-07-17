# apps/diagnosis/tasks.py
from celery import shared_task
from .models import Diagnosis
from .services import DiagnosisOrchestrationService
from .repositories import DiagnosisRepository
from .exceptions import DiagnosisError

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_diagnosis(self, diagnosis_id: str):
    """
    مهمة Celery غير متزامنة لتشغيل خط أنابيب التشخيص.
    """
    print(f"INFO: Celery task started for diagnosis ID: {diagnosis_id}")
    repo = DiagnosisRepository()
    try:
        diagnosis = Diagnosis.objects.get(id=diagnosis_id)
        # في نظام حقيقي، ستحصل على بيانات المريض الديموغرافية من هنا
        demographics = {"age": 45, "gender": "male"} # بيانات وهمية
        
        # يمكنك تمرير مسار الصورة، أو بيانات الصورة مباشرة إذا كانت صغيرة
        image_data = diagnosis.left_fundus_image.read() 
        
        service = DiagnosisOrchestrationService()
        result = service.run_full_diagnosis(image_data, demographics)

        repo.update_with_success(diagnosis_id, result)
        print(f"INFO: Successfully processed diagnosis ID: {diagnosis_id}")
    except Diagnosis.DoesNotExist:
        print(f"ERROR: Diagnosis ID {diagnosis_id} not found.")
    except DiagnosisError as e:
        print(f"ERROR: A non-retriable diagnosis error occurred: {e}")
        repo.update_with_failure(diagnosis_id, str(e))
    except Exception as e:
        # أخطاء غير متوقعة (مشاكل شبكة، إلخ.) -> أعد المحاولة
        print(f"ERROR: An unexpected error occurred. Retrying... Error: {e}")
        self.retry(exc=e)