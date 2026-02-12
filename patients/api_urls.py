from django.urls import path
from .api_views import PatientDetailAPI

urlpatterns = [
    path('patient/<str:token>/', PatientDetailAPI.as_view(), name='api_patient_detail'),
]
