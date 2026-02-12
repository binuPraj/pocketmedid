import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pocketmedid.settings')
django.setup()

from patients.models import Patient
from PIL import Image
from pyzbar.pyzbar import decode
import re

print("=" * 80)
print("COMPREHENSIVE QR CODE DIAGNOSTIC")
print("=" * 80)

# Check all patients
for p in Patient.objects.all():
    print(f"\n{'=' * 80}")
    print(f"Patient: {p} (ID: {p.id})")
    print(f"Access Token: {p.access_token}")
    print(f"{'=' * 80}")
    
    # 1. Check get_qr_url output
    qr_url = p.get_qr_url()
    print(f"\n1. QR URL from get_qr_url():")
    print(f"   {repr(qr_url)}")
    print(f"   Length: {len(qr_url)}")
    
    # 2. Check if QR code file exists
    if p.qr_code:
        qr_path = p.qr_code.path
        print(f"\n2. QR Code File:")
        print(f"   Filename: {p.qr_code.name}")
        print(f"   Full Path: {qr_path}")
        print(f"   Exists: {os.path.exists(qr_path)}")
        
        if os.path.exists(qr_path):
            # 3. Check image properties
            img = Image.open(qr_path)
            print(f"\n3. Image Properties:")
            print(f"   Size: {img.size}")
            print(f"   Format: {img.format}")
            print(f"   Mode: {img.mode}")
            
            # 4. Decode QR
            decoded = decode(img)
            print(f"\n4. QR Decode Result:")
            print(f"   Number of QR codes found: {len(decoded)}")
            
            if decoded:
                for i, qr in enumerate(decoded):
                    qr_data = qr.data.decode('utf-8')
                    print(f"\n   QR Code {i+1}:")
                    print(f"   Raw Data: {repr(qr_data)}")
                    print(f"   Data Length: {len(qr_data)}")
                    
                    # 5. Test regex
                    print(f"\n5. Regex Extraction:")
                    match = re.search(r'/patients/details/(\d+)/([a-fA-F0-9\-]+)/', qr_data)
                    if match:
                        print(f"   ✓ MATCH SUCCESS")
                        print(f"   Patient ID: {match.group(1)}")
                        print(f"   Token: {match.group(2)}")
                    else:
                        print(f"   ✗ REGEX FAILED")
                        print(f"   Trying to understand why...")
                        
                        # Check for URL pattern
                        if 'patients/details' in qr_data:
                            print(f"   - 'patients/details' found in QR data")
                        else:
                            print(f"   - 'patients/details' NOT found in QR data")
                        
                        if 'http' in qr_data:
                            print(f"   - 'http' found in QR data")
                        else:
                            print(f"   - 'http' NOT found in QR data")
                        
                        # Check for UUID pattern
                        uuid_pattern = r'[a-fA-F0-9\-]{36}'
                        uuid_match = re.search(uuid_pattern, qr_data)
                        if uuid_match:
                            print(f"   - UUID pattern found: {uuid_match.group()}")
                        else:
                            print(f"   - No UUID pattern found")
            else:
                print(f"   ✗ NO QR CODE FOUND IN IMAGE")
    else:
        print(f"\n✗ No QR code generated for this patient")

print(f"\n\n{'=' * 80}")
print("END OF DIAGNOSTIC")
print(f"{'=' * 80}")
