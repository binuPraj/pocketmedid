
# PocketMed ID - Django Application

A complete Django web application for digital healthcare records management with QR code-based patient data sharing.

## Features

### 👤 Patient Features
- **User Registration & Authentication**: Secure signup and login
- **Medical Profile**: Store personal info (name, age, blood group, address, phone)
- **Allergies Management**: Track and manage known allergies with severity levels
- **Chronic Conditions**: Record ongoing health conditions and their status
- **Emergency Contacts**: Save emergency contact information
- **Medical Records**: Upload and organize medical files, prescriptions, lab reports
- **Medication Tracking**: Keep track of current medications and dosages
- **QR Code Generation**: Auto-generated QR code for easy doctor access

### 👨‍⚕️ Doctor Features
- **QR Code Scanner**: Scan patient QR codes to access their data
- **Patient Summary**: View comprehensive patient health information
- **Allergies & Conditions**: See critical health information at a glance
- **Medical Timeline**: View recent medications and medical records
- **Scan History**: Track scanning history with patients

## Installation

### 1. Clone or Setup the Project
```bash
cd c:\Users\ASUS\OneDrive\Desktop\binu\pocketmedid
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Access the application at: `http://localhost:8000`
Admin panel: `http://localhost:8000/admin`

## Project Structure

```
pocketmedid/
├── core/                    # Core app (auth, home)
│   ├── models.py           # UserProfile model
│   ├── views.py            # Home, signup, login views
│   ├── urls.py             # Core URL patterns
│   ├── forms.py            # Auth forms
│   └── admin.py            # Admin configuration
├── patients/               # Patients app
│   ├── models.py           # Patient, Allergy, ChronicCondition, etc.
│   ├── views.py            # Patient profile, upload views
│   ├── urls.py             # Patient URL patterns
│   ├── forms.py            # Patient forms
│   └── admin.py            # Admin configuration
├── doctors/                # Doctors app
│   ├── models.py           # Doctor, ScanLog models
│   ├── views.py            # QR scan, patient summary views
│   ├── urls.py             # Doctor URL patterns
│   ├── forms.py            # Doctor forms
│   └── admin.py            # Admin configuration
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── core/               # Core templates
│   ├── patients/           # Patient templates
│   └── doctors/            # Doctor templates
├── static/                 # Static files
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   └── js/                 # JavaScript files
├── media/                  # User uploads (QR codes, records, etc.)
├── pocketmedid/            # Django project settings
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Database Models

### Core App
- **UserProfile**: Links User to patient/doctor type

### Patients App
- **Patient**: Main patient profile
- **Allergy**: Known allergies with severity
- **ChronicCondition**: Ongoing health conditions
- **EmergencyContact**: Emergency contact information
- **MedicalRecord**: Uploaded medical documents and images
- **Medicine**: Current medications and dosages

### Doctors App
- **Doctor**: Doctor profile with license and specialization
- **ScanLog**: History of QR code scans

## URL Routes

### Core (Home & Auth)
- `/` - Home page
- `/signup/` - Patient/Doctor signup
- `/login/` - Login
- `/logout/` - Logout
- `/patient-dashboard/` - Patient dashboard redirect
- `/doctor-dashboard/` - Doctor dashboard redirect

### Patients
- `/patients/profile/<id>/` - Patient profile
- `/patients/<id>/upload/` - Upload medical records
- `/patients/allergy/<id>/add/` - Add allergy
- `/patients/condition/<id>/add/` - Add condition
- `/patients/emergency-contact/<id>/add/` - Add contact

### Doctors
- `/doctors/scan/` - QR code scanner
- `/doctors/patient/<id>/summary/` - Patient health summary

## Screenshots & Features Implemented

✅ **Screen 1: Home** - "I am a patient" / "I am a doctor" buttons
✅ **Screen 2: Patient Signup/Login** - Complete authentication
✅ **Screen 3: Patient Profile** - All info + QR code card
✅ **Screen 4: Patient Upload** - Medical records + photo upload
✅ **Screen 5: Doctor Scan QR** - QR code scanning interface
✅ **Screen 6: Doctor Patient Summary** - Details, allergies, meds, timeline

## Key Features

- **QR Code Generation**: Automatic QR code creation for each patient
- **File Upload**: Support for medical documents and images
- **Responsive Design**: Bootstrap 5 for mobile-friendly interface
- **Admin Panel**: Complete Django admin for data management
- **User Authentication**: Django's built-in auth system
- **Data Validation**: Form validation and error handling

## Security Features

- CSRF Protection
- Password hashing
- User authentication required for sensitive views
- File upload validation
- SQL injection protection (Django ORM)

## Customization

### Styling
Edit `static/css/style.css` to customize colors and layout.

### Models
Add more fields to models in respective `models.py` files and run migrations.

### Templates
All templates use Bootstrap 5. Modify `templates/` directory for custom designs.

## Testing

### Create Test Data
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from core.models import UserProfile
from patients.models import Patient
from doctors.models import Doctor

# Create patient
user = User.objects.create_user(
    username='patient1',
    email='patient@example.com',
    first_name='John',
    last_name='Doe',
    password='testpass123'
)
UserProfile.objects.create(user=user, user_type='patient')
Patient.objects.create(user=user, age=30, blood_group='O+')

# Create doctor
doc_user = User.objects.create_user(
    username='doctor1',
    email='doctor@example.com',
    first_name='Jane',
    last_name='Smith',
    password='testpass123'
)
UserProfile.objects.create(user=doc_user, user_type='doctor')
Doctor.objects.create(
    user=doc_user,
    license_number='LIC123456',
    specialization='Cardiology'
)
```

## Deployment

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure allowed hosts
3. Set up proper database (PostgreSQL recommended)
4. Configure static files serving (WhiteNoise or CDN)
5. Use environment variables for sensitive settings
6. Enable HTTPS

## Support & Documentation

- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/
- QR Code Library: https://github.com/lincolnloop/python-qrcode

## License

This project is created for educational purposes.

---

**Created**: December 2024
**Django Version**: 5.1.3
**Python**: 3.8+
=======
# 🏥 PocketMedID

PocketMedID is a QR-based digital medical identity system that allows doctors to instantly access a patient’s essential medical history during emergencies.

Instead of carrying heavy medical files, patients simply present a QR code.  
Doctors scan the QR code and securely view allergies, chronic conditions, medications, and recent medical records.


## 🚨 Problem It Solves

- Patients often carry bulky medical documents.
- In emergencies, critical medical history is hard to access quickly.
- Important information like allergies or chronic conditions may be unavailable.
- Delays in treatment due to missing records.

PocketMedID solves this by digitizing patient records and making them accessible through secure QR scanning.


## 💡 How It Works

1. Each patient has a unique QR code.
2. The QR code contains a secure URL with an access token.
3. A doctor logs into the system.
4. The doctor scans or uploads the patient's QR code.
5. The system verifies the token.
6. The doctor can view a patient summary instantly.
7. Every scan is logged for security and auditing.


## 🔐 Security Features

- Token-based patient access verification
- Doctor authentication required
- Scan logging system (tracks who accessed which patient and when)
- Access control between patients and doctors


## 👨‍⚕️ Doctor Features

- Create doctor profile (license number, specialization, clinic details)
- Scan patient QR code
- View patient summary
- View scan history logs

---

## 👤 Patient Features

- Unique QR code generation
- Store:
  - Allergies
  - Chronic conditions
  - Medicines
  - Medical records
- Secure access via access token


## 🛠 Tech Stack

- **Backend:** Django
- **Database:** SQLite (can be upgraded to PostgreSQL)
- **Authentication:** Django Auth System
- **QR Code Generation:** `qrcode`
- **QR Code Scanning:** `pyzbar`
- **Image Processing:** Pillow



>>>>>>> ed2ff6e517e98c80c08c83d3cb670f214cfb8dbe
