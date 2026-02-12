from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import SignUpForm, LoginForm
from .models import UserProfile
from patients.models import Patient
from doctors.models import Doctor


def home(request):
    """Home screen with role selection"""
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
        except UserProfile.DoesNotExist:
            pass
    
    return render(request, 'core/home.html')


def signup(request):
    """User signup view"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            user_type = form.cleaned_data['user_type']
            UserProfile.objects.create(user=user, user_type=user_type)
            
            # Create patient or doctor profile
            if user_type == 'patient':
                Patient.objects.create(user=user)
                login(request, user)
                return redirect('patient_dashboard')
            else:
                Doctor.objects.create(user=user)
                login(request, user)
                return redirect('doctor_dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})


def login_view(request):
    """User login view"""
    next_url = request.GET.get('next') or request.POST.get('next')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # If ?next= is present, redirect there (for QR scan flow)
                if next_url:
                    return redirect(next_url)
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    if user_profile.user_type == 'patient':
                        return redirect('patient_dashboard')
                    else:
                        return redirect('doctor_dashboard')
                except UserProfile.DoesNotExist:
                    return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'core/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    """User logout view"""
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def patient_dashboard(request):
    """Patient dashboard redirect"""
    try:
        patient = Patient.objects.get(user=request.user)
        return redirect('patient_profile', pk=patient.id)
    except Patient.DoesNotExist:
        return redirect('home')


@login_required(login_url='login')
def doctor_dashboard(request):
    """Doctor dashboard redirect"""
    try:
        doctor = Doctor.objects.get(user=request.user)
        return redirect('doctor_scan')
    except Doctor.DoesNotExist:
        return redirect('home')
