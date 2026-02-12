from django.db import models
from django.contrib.auth.models import User
from patients.models import Patient

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100, unique=True)
    specialization = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, null=True, blank=True)
    clinic_address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


class ScanLog(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='scan_logs')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='scan_logs')
    scanned_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.doctor.user.first_name} scanned {self.patient.user.first_name}'s QR"
    
    class Meta:
        ordering = ['-scanned_at']
