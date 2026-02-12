from django import forms
from .models import Patient, Allergy, ChronicCondition, EmergencyContact, MedicalRecord


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('age', 'blood_group', 'phone', 'address')
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
        }


class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ('allergy_name', 'severity', 'description')
        widgets = {
            'allergy_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Allergy name'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Description'}),
        }


class ChronicConditionForm(forms.ModelForm):
    class Meta:
        model = ChronicCondition
        fields = ('condition_name', 'diagnosis_date', 'status', 'description')
        widgets = {
            'condition_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Condition name'}),
            'diagnosis_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Description'}),
        }


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ('name', 'relationship', 'phone')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact name'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        }


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ('record_type', 'title', 'description', 'file', 'photo', 'date_created')
        widgets = {
            'record_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Record title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Description'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'date_created': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
