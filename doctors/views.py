from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Doctor, ScanLog
from patients.models import Patient
import json
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import io
import re


@login_required(login_url='login')
def doctor_scan_qr(request):
    """Doctor QR scanner screen with upload option"""
    doctor = get_object_or_404(Doctor, user=request.user)
    error_message = None
    
    if request.method == 'POST' and 'qr_image' in request.FILES:
        qr_image = request.FILES['qr_image']
        
        try:
            # Reset file pointer to beginning
            qr_image.seek(0)
            
            # Open and decode QR code
            image = Image.open(qr_image)
            image.load()  # Force load to ensure image is valid
            
            decoded_objects = decode(image)
            
            qr_data = None
            if decoded_objects:
                # Try to find a QR code with the patient details URL
                for qr_code in decoded_objects:
                    decoded_text = qr_code.data.decode('utf-8')
                    # Check if this QR contains the patient details URL
                    if '/patients/details/' in decoded_text:
                        qr_data = decoded_text
                        break
                
                # Fallback to first QR code if no match found
                if not qr_data:
                    qr_data = decoded_objects[0].data.decode('utf-8')
            
            if qr_data:
                # Extract patient_id and token from URL
                # URL format: /patients/details/<id>/<token>/
                match = re.search(r'/patients/details/(\d+)/([a-fA-F0-9\-]+)/', qr_data)
                
                if match:
                    patient_id = int(match.group(1))
                    token = match.group(2)
                    
                    # Verify patient exists
                    try:
                        patient = Patient.objects.get(id=patient_id)
                        # Verify token matches
                        if patient.access_token == token:
                            # Log the scan
                            ScanLog.objects.create(doctor=doctor, patient=patient)
                            # Redirect to patient details view
                            return redirect('patient_details', patient_id=patient_id, token=token)
                        else:
                            error_message = 'Invalid QR code - Token mismatch'
                    except Patient.DoesNotExist:
                        error_message = f'Patient with ID {patient_id} not found'
                else:
                    error_message = 'Invalid QR code format - Could not extract patient details'
            else:
                error_message = 'No QR code found in image. Please upload a clear QR code image.'
                
        except Image.UnidentifiedImageError:
            error_message = 'Invalid image file. Please upload a valid image (PNG, JPG, etc.)'
        except Exception as e:
            error_message = f'Error processing QR code: {str(e)}'
    
    context = {
        'doctor': doctor,
        'error_message': error_message,
    }
    
    return render(request, 'doctors/scan_qr.html', context)


@login_required(login_url='login')
def process_qr_scan(request):
    """Process QR code data from scan (legacy)"""
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')
        
        try:
            # Parse URL format: /patients/details/<id>/<token>/
            match = re.search(r'/patients/details/(\d+)/([a-fA-F0-9\-]+)/', qr_data)
            
            if match:
                patient_id = int(match.group(1))
                token = match.group(2)
                
                doctor = get_object_or_404(Doctor, user=request.user)
                patient = get_object_or_404(Patient, id=patient_id)
                
                # Verify token
                if patient.access_token == token:
                    # Log the scan
                    ScanLog.objects.create(doctor=doctor, patient=patient)
                    
                    return redirect('patient_details', patient_id=patient_id, token=token)
                else:
                    return render(request, 'doctors/scan_qr.html', {
                        'error': 'Invalid or expired QR code'
                    })
            else:
                return render(request, 'doctors/scan_qr.html', {
                    'error': 'Invalid QR code format'
                })
                
        except Exception as e:
            return render(request, 'doctors/scan_qr.html', {
                'error': f'Error: {str(e)}'
            })
    
    return redirect('doctor_scan')


@login_required(login_url='login')
def patient_summary(request, patient_id):
    """Doctor view of patient summary"""
    patient = get_object_or_404(Patient, id=patient_id)
    doctor = get_object_or_404(Doctor, user=request.user)
    
    context = {
        'patient': patient,
        'doctor': doctor,
        'allergies': patient.allergies.all(),
        'chronic_conditions': patient.chronic_conditions.all(),
        'medicines': patient.medicines.all().order_by('-start_date')[:5],
        'medical_records': patient.medical_records.all()[:5],
        'scan_logs': ScanLog.objects.filter(patient=patient, doctor=doctor).order_by('-scanned_at')[:10],
    }
    
    return render(request, 'doctors/patient_summary.html', context)

