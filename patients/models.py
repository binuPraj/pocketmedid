from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
import json
import uuid
from django.urls import reverse

class Patient(models.Model):
    BLOOD_GROUP_CHOICES = (
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    access_token = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def generate_access_token(self):
        """Generate unique access token for patient"""
        if not self.access_token:
            self.access_token = str(uuid.uuid4())
            self.save()
        return self.access_token
    
    def get_qr_url(self, request=None):
        """Get the full URL for patient details page"""
        from django.contrib.sites.shortcuts import get_current_site
        from django.http import HttpRequest
        
        # Generate access token if not exists
        self.generate_access_token()
        
        # Build URL
        path = reverse('patient_details', kwargs={
            'patient_id': self.id,
            'token': self.access_token
        })
        
        if request:
            return request.build_absolute_uri(path)
        else:
            # Fallback URL
            return f"http://localhost:8000{path}"
    
    def generate_qr_code(self):
        # Generate access token first
        self.generate_access_token()
        
        # Get the full URL for patient details
        qr_url = self.get_qr_url()
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        file_name = f"qr_code_{self.id}.png"
        file_path = BytesIO()
        img.save(file_path, 'PNG')
        self.qr_code.save(file_name, File(file_path), save=False)


class Allergy(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='allergies')
    allergy_name = models.CharField(max_length=200)
    severity = models.CharField(max_length=20, choices=[('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe')])
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.user.first_name} - {self.allergy_name}"
    
    class Meta:
        verbose_name_plural = "Allergies"


class ChronicCondition(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='chronic_conditions')
    condition_name = models.CharField(max_length=200)
    diagnosis_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('resolved', 'Resolved')])
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.user.first_name} - {self.condition_name}"


class EmergencyContact(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.relationship})"


class MedicalRecord(models.Model):
    RECORD_TYPE_CHOICES = (
        ('prescription', 'Prescription'),
        ('lab_report', 'Lab Report'),
        ('imaging', 'Imaging'),
        ('consultation', 'Consultation'),
        ('other', 'Other'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='medical_records/')
    photo = models.ImageField(upload_to='medical_records/', null=True, blank=True)
    date_created = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.user.first_name} - {self.title}"
    
    class Meta:
        ordering = ['-date_created']


class Medicine(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medicines')
    medicine_name = models.CharField(max_length=300)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    prescribing_doctor = models.CharField(max_length=200, blank=True)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.user.first_name} - {self.medicine_name}"
