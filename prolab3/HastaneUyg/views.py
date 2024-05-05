from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Doctor


from .forms import DoctorForm
def home(request):
    return render(request, 'home.html')


def doctor_login(request):
    # Doktor giriş işlemleri
    return render(request, 'doctor_login.html')

def patient_login(request):
    # Hasta giriş işlemleri
    return render(request, 'patient_login.html')


def admin_login(request):
    if request.method == 'POST':
        # Kullanıcı adı ve şifreyi formdan al
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Kullanıcıyı doğrula
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Kullanıcı doğrulandıysa oturum aç
            login(request, user)
            # Başarılı giriş durumunda admin_page'e yönlendir
            return redirect('admin_page')
        else:
            # Hatalı giriş durumunda hata mesajını görüntüle
            return render(request, 'admin_login.html', {'error_message': 'Geçersiz kullanıcı adı veya şifre.'})
    else:
        # GET isteği ise sadece giriş formunu göster
        return render(request, 'admin_login.html')

@login_required
def admin_page(request):
    username = request.user.username
    return render(request, 'admin_page.html', {'username': username})


def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = DoctorForm()
    return render(request, 'doctor_create.html', {'form': form})



def list_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'list_doctors.html', {'doctors': doctors})

def delete_doctor(request, doctor_id):
    doctor = Doctor.objects.get(idDoctor=doctor_id)
    doctor.delete()
    return redirect('list_doctors')
