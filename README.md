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



