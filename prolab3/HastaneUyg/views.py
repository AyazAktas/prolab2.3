from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def doctor_login(request):
    # Doktor giriş işlemleri
    pass

def patient_login(request):
    # Hasta giriş işlemleri
    return render(request, 'patient_login.html')
def admin_login(request):
    # Yönetici giriş işlemleri
    pass
