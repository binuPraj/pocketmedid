from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse
from .models import Patient, Allergy, ChronicCondition, EmergencyContact, MedicalRecord, Medicine
from .forms import (
    PatientProfileForm, AllergyForm, ChronicConditionForm,
    EmergencyContactForm, MedicalRecordForm
)


@login_required(login_url='login')
def patient_profile(request, pk):
    """Patient profile view with all information"""
    patient = get_object_or_404(Patient, id=pk, user=request.user)
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            if not patient.qr_code:
                patient.generate_qr_code()
                patient.save()
            return redirect('patient_profile', pk=patient.id)
    else:
        form = PatientProfileForm(instance=patient)
    
    # Generate QR code if not exists
    if not patient.qr_code:
        patient.generate_qr_code()
        patient.save()
    
    context = {
        'patient': patient,
        'form': form,
        'allergies': patient.allergies.all(),
        'chronic_conditions': patient.chronic_conditions.all(),
        'emergency_contacts': patient.emergency_contacts.all(),
        'medicines': patient.medicines.all().order_by('-start_date'),
        'medical_records': patient.medical_records.all(),
    }
    
    return render(request, 'patients/profile.html', context)


@login_required(login_url='login')
def add_allergy(request, patient_id):
    """Add allergy to patient profile"""
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    
    if request.method == 'POST':
        form = AllergyForm(request.POST)
        if form.is_valid():
            allergy = form.save(commit=False)
            allergy.patient = patient
            allergy.save()
            return redirect('patient_profile', pk=patient_id)
    else:
        form = AllergyForm()
    
    return render(request, 'patients/add_allergy.html', {'form': form, 'patient': patient})


@login_required(login_url='login')
def add_chronic_condition(request, patient_id):
    """Add chronic condition to patient profile"""
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    
    if request.method == 'POST':
        form = ChronicConditionForm(request.POST)
        if form.is_valid():
            condition = form.save(commit=False)
            condition.patient = patient
            condition.save()
            return redirect('patient_profile', pk=patient_id)
    else:
        form = ChronicConditionForm()
    
    return render(request, 'patients/add_condition.html', {'form': form, 'patient': patient})


@login_required(login_url='login')
def add_emergency_contact(request, patient_id):
    """Add emergency contact"""
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.patient = patient
            contact.save()
            return redirect('patient_profile', pk=patient_id)
    else:
        form = EmergencyContactForm()
    
    return render(request, 'patients/add_emergency_contact.html', {'form': form, 'patient': patient})


@login_required(login_url='login')
def delete_allergy(request, allergy_id):
    """Delete allergy"""
    allergy = get_object_or_404(Allergy, id=allergy_id)
    patient = allergy.patient
    
    if request.user == patient.user:
        allergy.delete()
    
    return redirect('patient_profile', pk=patient.id)


@login_required(login_url='login')
def delete_condition(request, condition_id):
    """Delete chronic condition"""
    condition = get_object_or_404(ChronicCondition, id=condition_id)
    patient = condition.patient
    
    if request.user == patient.user:
        condition.delete()
    
    return redirect('patient_profile', pk=patient.id)


@login_required(login_url='login')
def delete_emergency_contact(request, contact_id):
    """Delete emergency contact"""
    contact = get_object_or_404(EmergencyContact, id=contact_id)
    patient = contact.patient
    
    if request.user == patient.user:
        contact.delete()
    
    return redirect('patient_profile', pk=patient.id)


@login_required(login_url='login')
def upload_records(request, patient_id):
    """Upload medical records and files"""
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            return redirect('patient_upload', patient_id=patient_id)
    else:
        form = MedicalRecordForm()
    
    context = {
        'patient': patient,
        'form': form,
        'medical_records': patient.medical_records.all(),
    }
    
    return render(request, 'patients/upload.html', context)


@login_required(login_url='login')
def delete_medical_record(request, record_id):
    """Delete medical record"""
    record = get_object_or_404(MedicalRecord, id=record_id)
    patient = record.patient
    
    if request.user == patient.user:
        record.delete()
    
    return redirect('patient_upload', patient_id=patient.id)


from doctors.models import Doctor
from django.contrib.auth.decorators import login_required

def patient_details(request, patient_id, token):
    """
    Patient details view accessed via QR code token
    Only shows details if valid token is provided and user is a doctor
    Read-only view for doctors
    """
    # If not logged in, redirect to login with next param
    if not request.user.is_authenticated:
        from django.urls import reverse
        next_url = reverse('patient_details', kwargs={'patient_id': patient_id, 'token': token})
        login_url = reverse('login')
        return redirect(f"{login_url}?next={next_url}")

    patient = get_object_or_404(Patient, id=patient_id)

    # Verify token
    if patient.access_token != token:
        return render(request, 'patients/access_denied.html', {
            'message': 'Invalid or expired access token'
        }, status=403)

    # Check if user is a doctor
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return render(request, 'patients/access_denied.html', {
            'message': 'Access restricted to authorized doctors only.'
        }, status=403)

    # Get patient data
    context = {
        'patient': patient,
        'allergies': patient.allergies.all(),
        'chronic_conditions': patient.chronic_conditions.all(),
        'emergency_contacts': patient.emergency_contacts.all(),
        'medicines': patient.medicines.all().order_by('-start_date'),
        'medical_records': patient.medical_records.all(),
        'is_read_only': True,  # Mark as read-only view
        'accessed_via_qr': True,
        'doctor': doctor,
    }

    return render(request, 'patients/patient_details_public.html', context)


@login_required(login_url='login')
def download_qr_code(request, patient_id):
    """Download patient's QR code image"""
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    
    # Generate QR if doesn't exist
    if not patient.qr_code:
        patient.generate_qr_code()
        patient.save()
    
    # Return the QR code image file
    if patient.qr_code:
        qr_file = patient.qr_code.open('rb')
        return FileResponse(qr_file, as_attachment=True, filename=f'patient_qr_{patient_id}.png')
    
    # Fallback if QR still doesn't exist
    return redirect('patient_profile', pk=patient_id)
