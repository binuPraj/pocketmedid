from django.contrib import admin
from .models import Doctor, ScanLog

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'specialization', 'phone', 'created_at')
    list_filter = ('specialization', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'license_number')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ScanLog)
class ScanLogAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'scanned_at')
    list_filter = ('scanned_at',)
    search_fields = ('doctor__user__first_name', 'patient__user__first_name')
    readonly_fields = ('scanned_at',)
