# apps/users/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Patient, Clinic



class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer لتسجيل مستخدم جديد."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # استخدم `create_user` لضمان تجزئة كلمة المرور بشكل صحيح
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', User.Roles.DOCTOR)
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    """Serializer لعرض بيانات المستخدم (بدون معلومات حساسة)."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role')


class ClinicSerializer(serializers.ModelSerializer):
    """Serializer للعيادات."""
    class Meta:
        model = Clinic
        fields = ('id', 'name', 'location', 'created_at')
        read_only_fields = ('id', 'created_at')

class PatientSerializer(serializers.ModelSerializer):
    """Serializer للمرضى، مع تضمين بيانات العيادة."""
    clinic = ClinicSerializer(read_only=True)
    clinic_id = serializers.UUIDField(write_only=True)
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Patient
        fields = ('id', 'full_name', 'date_of_birth', 'gender', 'age', 'clinic', 'clinic_id', 'doctors')
        read_only_fields = ('id', 'clinic')
    
    def create(self, validated_data):
        # ربط الطبيب الذي أنشأ المريض تلقائيًا
        doctor = self.context['request'].user
        patient = super().create(validated_data)
        patient.doctors.add(doctor)
        return patient