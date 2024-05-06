from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Doctor, Hasta
from django.shortcuts import get_object_or_404
from .forms import PatientRegistrationForm


from .forms import DoctorForm,PatientForm
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

def patient_register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or any other page you want
            return redirect('patient_login')
    else:
        form = PatientRegistrationForm()
    return render(request, 'patient_register.html', {'form': form})



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


def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = PatientForm()
    return render(request, 'patient_create.html', {'form': form})


def list_patients(request):
    patients = Hasta.objects.all()
    return render(request, 'list_patients.html', {'patients': patients})


def delete_patient(request, patient_id):
    patient = get_object_or_404(Hasta, idHasta=patient_id)
    patient.delete()
    return redirect('list_patients')

@login_required

def patient_login(request):
    if request.method == 'POST':
        hasta_ad_soyad = request.POST.get('hasta_ad_soyad')
        hasta_id = request.POST.get('hasta_id')

        # Kullanıcı adı olarak girilen değeri idHasta alanı ile karşılaştır
        try:
            hasta = Hasta.objects.get(idHasta=hasta_id)

            # Kullanıcı adı olarak girilen değeri ad ve soyad alanlarına bölelim
            ad_soyad = hasta_ad_soyad.split()
            hasta_adi = ad_soyad[0]
            hasta_soyadi = ' '.join(ad_soyad[1:])  # Soyad, boşluklarla ayrılmış tüm parçaları birleştir

            # Ad ve soyadı veritabanındaki kayıtla karşılaştır
            if hasta.hastaAdi == hasta_adi and hasta.hastaSoyadi == hasta_soyadi:
                return redirect('patient_page', id=hasta.idHasta)
            else:
                error_message = 'Geçersiz kullanıcı adı veya şifre.'
                return render(request, 'patient_login.html', {'error_message': error_message})
        except Hasta.DoesNotExist:
            error_message = 'Geçersiz kullanıcı adı veya şifre.'
            return render(request, 'patient_login.html', {'error_message': error_message})
    else:
        return render(request, 'patient_login.html')

def patient_page(request, id):
    hasta = Hasta.objects.get(idHasta=id)
    return render(request, 'patient_page.html', {'hasta': hasta})

def patient_info(request, hasta_id):
    # Hasta bilgilerini getir
    hasta = Hasta.objects.get(idHasta=hasta_id)

    if request.method == 'POST':
        # Formdan gelen verilerle hasta bilgilerini güncelle
        form = PatientForm(request.POST, instance=hasta)
        if form.is_valid():
            form.save()
            # Hasta bilgileri başarıyla güncellendikten sonra patient_page'e yönlendir
            return redirect('patient_page', id=hasta_id)
    else:
        # GET isteği ise formu göster
        form = PatientForm(instance=hasta)

        # Doğum tarihi ve cinsiyet alanlarını formda devre dışı bırak
        form.fields['idHasta'].disabled=True
        form.fields['dogumTarihi'].disabled = True
        form.fields['cinsiyet'].disabled = True

    return render(request, 'patient_info.html', {'form': form, 'hasta': hasta})