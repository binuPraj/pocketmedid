import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pocketmedid.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from io import BytesIO

print("\n" + "=" * 80)
print("SIMULATING DOCTOR QR UPLOAD")
print("=" * 80)

# Create test client
client = Client()

# Get or create a doctor user
try:
    doctor_user = User.objects.get(username='doctor_user')
except User.DoesNotExist:
    print("\nNo doctor user found. Creating one...")
    doctor_user = User.objects.create_user(
        username='doctor_user',
        password='testpass123',
        first_name='Test',
        last_name='Doctor'
    )
    doctor, created = Doctor.objects.get_or_create(user=doctor_user)
    print(f"Created doctor user and profile")

# Get the first patient's QR code
patient = Patient.objects.first()
if not patient or not patient.qr_code:
    print("ERROR: No patient with QR code found")
    exit()

print(f"\nUsing patient: {patient}")
print(f"Patient QR file: {patient.qr_code.path}")

# Read the QR code image
qr_path = patient.qr_code.path
with open(qr_path, 'rb') as f:
    qr_image_data = f.read()

print(f"QR file size: {len(qr_image_data)} bytes")

# Login as doctor
login_success = client.login(username='doctor_user', password='testpass123')
print(f"\nDoctor login: {'✓ Success' if login_success else '✗ Failed'}")

# Prepare file upload
from django.core.files.uploadedfile import SimpleUploadedFile

qr_file = SimpleUploadedFile(
    "qr_code_test.png",
    qr_image_data,
    content_type="image/png"
)

# POST to doctor scan endpoint
print("\nUploading QR code...")
response = client.post('/doctors/scan/', {'qr_image': qr_file}, follow=False)

print(f"Response Status: {response.status_code}")
print(f"Response URL: {response.url if hasattr(response, 'url') else 'N/A'}")

if response.status_code == 302:
    print(f"✓ REDIRECT - Expected redirect to patient details")
    print(f"  Redirect to: {response.url}")
else:
    print(f"Response contains error message - checking content...")
    if b'error_message' in response.content or b'Error' in response.content:
        print(f"✓ Form re-rendered with error")
        # Look for error message in content
        if b'Invalid QR code format' in response.content:
            print(f"  Error: Invalid QR code format")
        elif b'No QR code found' in response.content:
            print(f"  Error: No QR code found in image")
        else:
            print(f"  Error: Unknown error")

print("\n" + "=" * 80)
