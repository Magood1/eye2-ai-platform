# apps/diagnosis/tests.py
from django.test import TestCase
from unittest.mock import patch
from apps.diagnosis.services import DiagnosisOrchestrationService, VisionModelService, TabularModelService
from apps.diagnosis.exceptions import ModelInferenceError

class DiagnosisServiceTests(TestCase):

    @patch.object(TabularModelService, 'predict')
    @patch.object(VisionModelService, 'predict')
    def test_orchestration_service_success_path(self, mock_vision_predict, mock_tabular_predict):
        """
        اختبار مسار النجاح لمنسق التشخيص.
        """
        mock_vision_predict.return_value = {"disease_probability": 0.8}
        mock_tabular_predict.return_value = {"final_diagnosis": "Test Disease", "confidence": 0.9}

        service = DiagnosisOrchestrationService()
        result = service.run_full_diagnosis(image_data=b'fake_image_bytes', demographics={})

        mock_vision_predict.assert_called_once()
        mock_tabular_predict.assert_called_once()
        self.assertEqual(result['final_diagnosis'], "Test Disease")

    @patch.object(VisionModelService, 'predict', side_effect=ModelInferenceError("GPU Out of Memory"))
    def test_orchestration_service_handles_inference_error(self, mock_vision_predict):
        """
        اختبار أن الخدمة تعالج الأخطاء القادمة من نماذج الذكاء الاصطناعي برشاقة.
        """
        service = DiagnosisOrchestrationService()

        with self.assertRaises(ModelInferenceError):
            service.run_full_diagnosis(image_data=b'', demographics={})

        mock_vision_predict.assert_called_once()
