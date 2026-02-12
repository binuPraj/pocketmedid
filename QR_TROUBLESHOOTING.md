# QR Code Scanning Troubleshooting Guide

## Issue: "Invalid QR Format" Error

This guide helps diagnose why doctors are getting "Invalid QR Format" errors when scanning patient QR codes.

## ✅ What Should Happen

1. Patient logs in and views their profile
2. Patient sees their QR code in the profile
3. Patient downloads/saves the QR code image
4. Doctor logs in and goes to "Scan Patient QR Code" page
5. Doctor uploads the QR code image
6. Doctor is shown the patient's read-only health details

## 🔍 Troubleshooting Steps

### Step 1: Verify Patient Has QR Code
- [ ] Patient logs into their profile: `/patients/profile/1/`
- [ ] Patient should see a QR code image displayed
- [ ] If no QR code is visible, the patient profile page should generate it

### Step 2: Check QR Code Content
The QR code should encode a URL in this format:
```
http://localhost:8000/patients/details/<patient_id>/<unique_token>/
```

Example:
```
http://localhost:8000/patients/details/1/23a34f42-2d18-4f57-8162-03d18661f5f2/
```

### Step 3: Verify File Upload
- [ ] Doctor selects a QR code image file (PNG, JPG, GIF)
- [ ] File should be less than 10MB
- [ ] File should be a clear, readable image

### Step 4: Check Image Quality
- [ ] QR code in image should be at least 100x100 pixels
- [ ] QR code should be fully visible in the image
- [ ] Image should not be blurry or damaged

## ⚠️ Common Issues

### Issue: "No QR code found in image"
- **Cause**: The image doesn't contain a readable QR code
- **Solution**: 
  - Make sure the QR code is fully visible in the image
  - Try a different image format (PNG works best)
  - Ensure the image is clear and not blurry

### Issue: "Invalid QR code format - Could not extract patient details"
- **Cause**: The QR code doesn't contain the expected URL format
- **Solution**:
  - Make sure you're uploading a QR code from this PocketMed ID system
  - Don't use QR codes from other sources
  - The QR code must be from the patient's profile page

### Issue: "Invalid QR code - Token mismatch for patient"
- **Cause**: The token in the QR code doesn't match the patient's current token
- **Solution**:
  - Patient's token may have been regenerated
  - Get a fresh QR code from the patient's profile
  - Don't use old/expired QR codes

### Issue: "Patient with ID X not found"
- **Cause**: The patient ID in the QR code doesn't exist in the database
- **Solution**:
  - Make sure the correct patient's QR code is being scanned
  - Check if the patient account still exists

## 🛠️ Database Reset (if needed)

If you need to regenerate all QR codes:

```bash
python manage.py shell
```

Then in the shell:
```python
from patients.models import Patient
from PIL import Image
from pyzbar.pyzbar import decode
import os

for patient in Patient.objects.all():
    if patient.qr_code:
        qr_path = patient.qr_code.path
        if os.path.exists(qr_path):
            os.remove(qr_path)
        patient.qr_code.delete()
    
    # Regenerate
    patient.generate_access_token()
    patient.generate_qr_code()
    patient.save()
    print(f"✓ {patient} - Token: {patient.access_token}")
```

## 📊 Testing Checklist

- [ ] Patient profile displays QR code
- [ ] QR code can be saved/downloaded
- [ ] Doctor can upload QR code image
- [ ] QR code is successfully decoded
- [ ] Patient details are displayed (read-only)
- [ ] Scan is logged in database

## 🆘 Still Having Issues?

1. Check Django console for error messages
2. Verify pyzbar is installed: `pip list | grep pyzbar`
3. Ensure MEDIA_ROOT and MEDIA_URL are correctly configured in settings.py
4. Check that media folder has correct permissions
5. Verify patient has a valid access_token in database
