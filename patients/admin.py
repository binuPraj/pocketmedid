from django.contrib import admin
from .models import Patient, Allergy, ChronicCondition, EmergencyContact, MedicalRecord, Medicine

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'blood_group', 'phone', 'created_at')
    list_filter = ('blood_group', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'phone')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'allergy_name', 'severity', 'created_at')
    list_filter = ('severity', 'created_at')
    search_fields = ('patient__user__first_name', 'allergy_name')

@admin.register(ChronicCondition)
class ChronicConditionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'condition_name', 'status', 'diagnosis_date')
    list_filter = ('status', 'diagnosis_date')
    search_fields = ('patient__user__first_name', 'condition_name')

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'patient', 'relationship', 'phone')
    search_fields = ('name', 'patient__user__first_name', 'phone')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'record_type', 'date_created', 'uploaded_at')
    list_filter = ('record_type', 'date_created', 'uploaded_at')
    search_fields = ('title', 'patient__user__first_name')

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'patient', 'dosage', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('medicine_name', 'patient__user__first_name')
