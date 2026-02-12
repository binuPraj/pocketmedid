from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:pk>/', views.patient_profile, name='patient_profile'),
    path('<int:patient_id>/upload/', views.upload_records, name='patient_upload'),
    path('details/<int:patient_id>/<str:token>/', views.patient_details, name='patient_details'),
    path('<int:patient_id>/download-qr/', views.download_qr_code, name='download_qr'),
    path('allergy/<int:patient_id>/add/', views.add_allergy, name='add_allergy'),
    path('allergy/<int:allergy_id>/delete/', views.delete_allergy, name='delete_allergy'),
    path('condition/<int:patient_id>/add/', views.add_chronic_condition, name='add_condition'),
    path('condition/<int:condition_id>/delete/', views.delete_condition, name='delete_condition'),
    path('emergency-contact/<int:patient_id>/add/', views.add_emergency_contact, name='add_emergency_contact'),
    path('emergency-contact/<int:contact_id>/delete/', views.delete_emergency_contact, name='delete_emergency_contact'),
    path('record/<int:record_id>/delete/', views.delete_medical_record, name='delete_medical_record'),
]
