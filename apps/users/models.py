# apps/users/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    """
    نموذج المستخدم المخصص الذي يوسع النموذج الافتراضي في Django.
    ملاحظة: حقول first_name, last_name, email موجودة بالفعل في AbstractUser.
    """
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        DOCTOR = "DOCTOR", "Doctor"

    # الحقول الإضافية
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.DOCTOR
    )
    # ملاحظة: سنزيل specialty و phone حاليًا للحفاظ على البساطة،
    # ويمكن إضافتها لاحقًا.



class Clinic(models.Model):
    """يمثل عيادة أو مستشفى."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Patient(models.Model):
    """يمثل سجل المريض."""
    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=Gender.choices)
    
    # علاقة المريض بالعيادة
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, related_name="patients")
    
    # علاقة المريض بالأطباء (متعدد إلى متعدد)
    doctors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="patients",
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def __str__(self):
        return self.full_name