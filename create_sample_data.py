#!/usr/bin/env python
"""
Script to create sample data for testing PocketMed ID
Run with: python manage.py shell < create_sample_data.py
"""

from django.contrib.auth.models import User
from core.models import UserProfile
from patients.models import Patient, Allergy, ChronicCondition, EmergencyContact, Medicine
from doctors.models import Doctor

# Create Patient User
patient_user = User.objects.create_user(
    username='patient_demo',
    email='patient@example.com',
    first_name='John',
    last_name='Doe',
    password='Patient@123'
)

# Create UserProfile for patient
UserProfile.objects.create(user=patient_user, user_type='patient')

# Create Patient Profile
patient = Patient.objects.create(
    user=patient_user,
    age=35,
    blood_group='O+',
    phone='+1 (555) 123-4567',
    address='123 Main Street, Springfield, IL 62701'
)

# Generate QR Code
patient.generate_qr_code()
patient.save()

# Add Allergies
Allergy.objects.create(
    patient=patient,
    allergy_name='Penicillin',
    severity='severe',
    description='Severe anaphylactic reaction to penicillin antibiotics'
)

Allergy.objects.create(
    patient=patient,
    allergy_name='Shellfish',
    severity='moderate',
    description='Causes hives and difficulty breathing'
)

# Add Chronic Conditions
ChronicCondition.objects.create(
    patient=patient,
    condition_name='Type 2 Diabetes',
    diagnosis_date='2020-06-15',
    status='active',
    description='Managed with Metformin and lifestyle changes'
)

ChronicCondition.objects.create(
    patient=patient,
    condition_name='Hypertension',
    diagnosis_date='2018-03-20',
    status='active',
    description='Controlled with Lisinopril 10mg daily'
)

# Add Emergency Contacts
EmergencyContact.objects.create(
    patient=patient,
    name='Sarah Doe',
    relationship='Spouse',
    phone='+1 (555) 987-6543'
)

EmergencyContact.objects.create(
    patient=patient,
    name='Robert Doe',
    relationship='Son',
    phone='+1 (555) 654-3210'
)

# Add Medications
Medicine.objects.create(
    patient=patient,
    medicine_name='Metformin',
    dosage='500mg',
    frequency='Twice daily',
    start_date='2020-06-15',
    prescribing_doctor='Dr. Smith',
    reason='Type 2 Diabetes management'
)

Medicine.objects.create(
    patient=patient,
    medicine_name='Lisinopril',
    dosage='10mg',
    frequency='Once daily',
    start_date='2018-03-20',
    prescribing_doctor='Dr. Johnson',
    reason='Blood pressure control'
)

print("✓ Patient demo account created!")
print(f"  Username: patient_demo")
print(f"  Email: patient@example.com")
print(f"  Password: Patient@123")

# Create Doctor User
doctor_user = User.objects.create_user(
    username='doctor_demo',
    email='doctor@example.com',
    first_name='Jane',
    last_name='Smith',
    password='Doctor@123'
)

# Create UserProfile for doctor
UserProfile.objects.create(user=doctor_user, user_type='doctor')

# Create Doctor Profile
doctor = Doctor.objects.create(
    user=doctor_user,
    license_number='MD-123456789',
    specialization='Internal Medicine',
    phone='+1 (555) 444-5555',
    clinic_address='456 Medical Plaza, Springfield, IL 62701'
)

print("✓ Doctor demo account created!")
print(f"  Username: doctor_demo")
print(f"  Email: doctor@example.com")
print(f"  Password: Doctor@123")

print("\n✓ Sample data created successfully!")
print("\nYou can now login and test the application:")
print("  Patient Portal: http://localhost:8000/login")
print("  Admin Panel: http://localhost:8000/admin")
