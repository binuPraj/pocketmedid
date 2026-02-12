from django import forms
from .models import Doctor


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('license_number', 'specialization', 'phone', 'clinic_address')
        widgets = {
            'license_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'License number'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specialization'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'clinic_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Clinic address'}),
        }
