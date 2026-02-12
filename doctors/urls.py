from django.urls import path
from . import views

urlpatterns = [
    path('scan/', views.doctor_scan_qr, name='doctor_scan'),
    path('scan/process/', views.process_qr_scan, name='process_qr_scan'),
    path('patient/<int:patient_id>/summary/', views.patient_summary, name='patient_summary'),
]
