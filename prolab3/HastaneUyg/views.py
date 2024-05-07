from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.db import connection
from django.shortcuts import redirect, render, get_object_or_404

from .forms import (DoctorForm, PatientForm, PatientRegistrationForm, RandevuForm)
from .models import Doctor


def home(request):
    return render(request, 'home.html')


def doctor_login(request):
    # Doktor giriş işlemleri
    if request.method == 'POST':
        doktor_ad_soyad = request.POST.get('doktor_ad_soyad')
        doktor_id = request.POST.get('doktor_id')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM doktorlar WHERE idDoctor = %s AND AD = %s AND SOYAD = %s", [doktor_id, doktor_ad_soyad.split()[0], ' '.join(doktor_ad_soyad.split()[1:])])
            doctor = cursor.fetchone()

        if doctor:
            return redirect('doctor_page', doktor_id=doctor[1])
        error_message = 'Geçersiz kullanıcı adı veya şifre.'
        return render(request, 'doctor_login.html', {'error_message': error_message})
    else:
        return render(request, 'doctor_login.html')

def doctor_page(request, doktor_id):
    doctor = get_object_or_404(Doctor, idDoctor=doktor_id)
    return render(request, 'doctor_page.html', {'doctor': doctor})



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
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO doktorlar (idDoctor,AD, SOYAD, UzmanlikAlani,CalismaYeri) VALUES (%s,%s, %s,%s,%s)", [data['idDoctor'],data['AD'],data['SOYAD'], data['UzmanlikAlani'],data['CalismaYeri']])
            return redirect('admin_page')
    else:
        form = DoctorForm()
    return render(request, 'doctor_create.html', {'form': form})

from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest


def list_doctors(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM doktorlar")
            doctors = cursor.fetchall()
            if not doctors:
                return HttpResponse("Doktor listesi boş.")
            else:
                return render(request, 'list_doctors.html', {'doctors': doctors})
    except Exception as e:
        return HttpResponse(f"Hata oluştu: {e}")

def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO hastalar (idHasta, hastaAdi, hastaSoyadi, dogumTarihi, cinsiyet, telefonNo, adres) VALUES (%s, %s, %s, %s, %s, %s, %s)", [data['idHasta'], data['hastaAdi'], data['hastaSoyadi'], data['dogumTarihi'], data['cinsiyet'], data['telefonNo'], data['adres']])

            return redirect('admin_page')
    else:
        form = PatientForm()
    return render(request, 'patient_create.html', {'form': form})

def list_patients(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM hastalar")
        patients = cursor.fetchall()
        print(patients)  # patients değişkenini kontrol etmek için
    return render(request, 'list_patients.html', {'patients': patients})

from django.db import connection


 # Assuming PostgreSQL

def delete_doctor(request, doctor_id):
    if request.method == 'POST':
        cursor = connection.cursor()

        try:
            cursor.execute("DELETE FROM doktorlar WHERE id = %s", (doctor_id,))
            connection.commit()
            # Redirect to doctor list page (assuming you have a URL pattern for it)
            return redirect('list_doctors')
        except Exception as e:
            # Handle errors appropriately (e.g., log the error, return an error message)
            print(f"Error deleting doctor: {e}")
            return render(request, 'list_doctors.html', {'error': 'Doktor silinemedi.'})
        finally:
            cursor.close()
            connection.close()
    else:
        return render(request, 'list_doctors.html', {'error': 'Geçersiz istek.'})


from django.shortcuts import redirect, render
from .models import Hasta  # Assuming your patient model is named 'Hasta'

def delete_patient(request, hasta_id):
    if request.method == 'POST':
        try:
            hasta = Hasta.objects.get(pk=hasta_id)
            hasta.delete()
            # Redirect to patient list page (assuming you have a URL pattern for it)
            return redirect('list_patients')
        except Hasta.DoesNotExist:
            # Return an error message or redirect to an error page
            return render(request, 'patient_list.html', {'error': 'Hasta bulunamadı.'})
        except Exception as e:
            # Log the error and return an appropriate error response
            print(f"Error deleting patient: {e}")
            return HttpResponseBadRequest('There was an error deleting the patient.')
    else:
        return render(request, 'patient_list.html', {'error': 'Geçersiz istek.'})




def patient_login(request):
    if request.method == 'POST':
        hasta_ad_soyad = request.POST.get('hasta_ad_soyad')
        hasta_id = request.POST.get('hasta_id')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM hastalar WHERE idHasta = %s", [hasta_id])
            hasta = cursor.fetchone()

        if hasta:
            ad_soyad = hasta_ad_soyad.split()
            hasta_adi = ad_soyad[0]
            hasta_soyadi = ' '.join(ad_soyad[1:])
            if hasta[2] == hasta_adi and hasta[3] == hasta_soyadi:
                return redirect('patient_page', id=hasta[1])
        error_message = 'Geçersiz kullanıcı adı veya şifre.'
        return render(request, 'patient_login.html', {'error_message': error_message})
    else:
        return render(request, 'patient_login.html')


def patient_page(request, id):
    hasta = get_object_or_404(Hasta, idHasta=id)
    return render(request, 'patient_page.html', {'hasta': hasta})

def patient_info(request, hasta_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM hastalar WHERE idHasta = %s", [hasta_id])
        hasta = cursor.fetchone()

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                # Güncelleme sorgusunu düzenleyelim
                cursor.execute("UPDATE hastalar SET  hastaAdi = %s, hastaSoyadi = %s, dogumTarihi = %s,  telefonNo = %s, adres = %s WHERE idHasta = %s",
                               [data['hastaAdi'], data['hastaSoyadi'], data['dogumTarihi'], data['telefonNo'], data['adres'], hasta_id])
                connection.commit()  # Veritabanında değişiklikleri kalıcı hale getir
            return redirect('patient_page', id=hasta_id)
    else:
        # Burada formun başlangıç verilerini hasta bilgilerinden doğru şekilde ayarlayın
        form = PatientForm(initial={
            'idHasta': hasta[1],
            'hastaAdi': hasta[2],
            'hastaSoyadi': hasta[3],
            'dogumTarihi': hasta[4],
            'cinsiyet': hasta[5],
            'telefonNo': hasta[6],
            'adres': hasta[7]
        })

    return render(request, 'patient_info.html', {'form': form, 'hasta': hasta})


from django.shortcuts import render, redirect
from .models import Randevu, Hasta, Doctor
from django.utils import timezone
from datetime import datetime


def randevu_al(request, hasta_id):
    if request.method == 'POST':
        # Formdan gelen verileri al
        randevu_tarihi = request.POST.get('randevu_tarihi')
        randevu_saat = request.POST.get('randevu_saat')
        doktor_id = request.POST.get('doktor_id')  # Kullanıcının seçtiği doktor ID'si

        # Doktorun varlığını kontrol et
        try:
            doktor = Doctor.objects.get(idDoctor=doktor_id)
        except Doctor.DoesNotExist:
            return HttpResponse("Geçersiz doktor ID.")

        # Randevu saati için uygun formata dönüştürme
        randevu_saati_str = f"{randevu_tarihi} {randevu_saat}"
        try:
            randevu_saati = datetime.strptime(randevu_saati_str, '%Y-%m-%d %H:%M')
        except ValueError:
            return HttpResponse("Geçersiz randevu saati formatı.")

        # Hasta bilgisini al
        hasta = Hasta.objects.get(idHasta=hasta_id)

        # Yeni bir Randevu oluştur ve kaydet
        randevu = Randevu(randevuTarihi=randevu_tarihi, randevuSaati=randevu_saati, idHasta=hasta, idDoctor=doktor)
        randevu.save()

        # Randevu alındıktan sonra başka bir sayfaya yönlendir
        return redirect('patient_page', id=hasta_id)
    else:
        # Tüm doktorları al ve kullanıcıya seçenek olarak sun
        doktorlar = Doctor.objects.all()
        return render(request, 'randevu_al.html', {'doktorlar': doktorlar})