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

from .forms import DoctorForm

def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, idDoctor=doctor_id)

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('list_doctors')  # Doktorlar listesi sayfasına yönlendir
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'edit_doctor.html', {'form': form, 'doctor': doctor})

def edit_patient(request, hasta_id):
    # Hasta objesini al
    hasta = get_object_or_404(Hasta, idHasta=hasta_id)

    if request.method == 'POST':
        # Formu POST verileriyle doldur
        form = PatientForm(request.POST, instance=hasta)
        if form.is_valid():
            # Form doğru şekilde doldurulduysa, değişiklikleri kaydet
            form.save()
            # Başarılı güncelleme sonrasında başka bir sayfaya yönlendirme yapabilirsiniz
            return redirect('patient_list')  # veya başka bir sayfa
    else:
        # GET isteği ise, formu hasta bilgileriyle doldur
        form = PatientForm(instance=hasta)

    return render(request, 'edit_patient.html', {'form': form})
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

from django.db import IntegrityError

def delete_doctor(request, doctor_id):
    if request.method == 'POST':
        cursor = connection.cursor()

        try:
            # Check if the doctor has any appointments
            cursor.execute("SELECT COUNT(*) FROM randevular WHERE doktor_id = %s", (doctor_id,))
            appointment_count = cursor.fetchone()[0]

            if appointment_count > 0:
                # If the doctor has appointments, prevent deletion and display a message
                return render(request, 'list_doctors.html', {'error': 'Doktorunuz randevusu olduğu için silinemez.'})

            # If the doctor has no appointments, proceed with deletion
            cursor.execute("DELETE FROM doktorlar WHERE id = %s", (doctor_id,))
            connection.commit()

            # Redirect to doctor list page
            return redirect('list_doctors')

        except IntegrityError:
            # If there is an integrity error (e.g., foreign key constraint violation), handle it appropriately
            return render(request, 'list_doctors.html', {'error': 'Doktor silinemedi.'})

        except Exception as e:
            # Handle other errors appropriately (e.g., log the error)
            print(f"Error deleting doctor: {e}")
            return render(request, 'list_doctors.html', {'error': 'Bir hata oluştu.'})

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
        try:
            hasta = Hasta.objects.get(idHasta=hasta_id)
        except Hasta.DoesNotExist:
            return HttpResponse("Geçersiz hasta ID.")

        # Yeni bir Randevu oluştur ve kaydet
        randevu = Randevu(randevuTarihi=randevu_tarihi, randevu_saati=randevu_saat, doktor_id=doktor_id, hasta_id=hasta_id)
        randevu.save()

        # Randevu alındıktan sonra başka bir sayfaya yönlendir
        return redirect('patient_page', id=hasta_id)
    else:
        # Tüm doktorları al ve kullanıcıya seçenek olarak sun
        doktorlar = Doctor.objects.all()
        return render(request, 'randevu_al.html', {'doktorlar': doktorlar})


def randevularim(request, hasta_id):
    # Hasta ID'sine göre randevuları filtrele
    randevular = Randevu.objects.filter(hasta_id=hasta_id)

    # Randevuların her biri için ilgili doktor bilgisini ekleyin
    for randevu in randevular:
        randevu.doktor = Doctor.objects.get(idDoctor=randevu.doktor_id)

    # Randevuları HTML sayfasına aktar ve göster
    return render(request, 'randevularim.html', {'randevular': randevular})

from django.shortcuts import get_object_or_404, redirect
from .models import Randevu

from django.shortcuts import get_object_or_404, redirect
from .models import Randevu

def randevu_sil(request, randevu_id):
    randevu = get_object_or_404(Randevu, randevuId=randevu_id)
    if request.method == 'POST':
        randevu.delete()
        return redirect('randevularim', hasta_id=randevu.hasta_id)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Randevu, Hasta


def rapor_yazilabilir(request, doktor_id):
    randevular = Randevu.objects.filter(doktor_id=doktor_id)

    for randevu in randevular:
        randevu.hasta = Hasta.objects.get(idHasta=randevu.hasta_id)

    return render(request, 'rapor_yazilabilir.html', {'randevular': randevular})
from django.shortcuts import render, redirect
from .forms import RaporForm
from .models import Randevu


from django.shortcuts import render, redirect
from .models import Randevu,TibbiRaporlar
from django.contrib import messages
from datetime import datetime

from django.shortcuts import get_object_or_404

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Randevu, Doctor, TibbiRaporlar
from .forms import RaporForm

def rapor_yaz(request, randevu_id):

    randevu = get_object_or_404(Randevu, pk=randevu_id)
    doktor_id = randevu.doktor_id
    doctor = get_object_or_404(Doctor, pk=doktor_id)
    hasta_id = randevu.hasta_id  # Hasta'nın ID'sine erişim

    if request.method == "POST":
        form = RaporForm(request.POST)  # Formu POST verileriyle oluştur
        if form.is_valid():  # Form doğru şekilde doldurulduysa
            uzmanlik_alani = doctor.UzmanlikAlani
            rapor = form.save(commit=False)
            rapor.doktor_id = doktor_id
            rapor.hasta_id = hasta_id
            rapor.uzmanlikAlani = uzmanlik_alani
            rapor.save()
            messages.success(request, "Rapor başarıyla gönderildi!")
            # Başarılı gönderimden sonra başka bir sayfaya yönlendirme yapabilirsiniz
        else:
            # Form geçerli değil, hataları göster
            print(form.errors)

    return render(
        request,
        "rapor_yaz.html",
        {
            "randevu": randevu,
            "hasta_id": hasta_id,
            "form": form,  # Formu template'e gönder
        },
    )
from django.shortcuts import render
from .models import TibbiRaporlar

def raporlarim(request, hasta_id):
    raporlar = TibbiRaporlar.objects.filter(hasta_id=hasta_id)
    return render(request, 'raporlarim.html', {'raporlar': raporlar})


# views.py

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import TibbiRaporlar, Hasta, Doctor


def raporlarim_pdf(request, rapor_id):
    rapor = TibbiRaporlar.objects.get(idRapor=rapor_id)
    hasta = Hasta.objects.get(idHasta=rapor.hasta_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{hasta.hastaAdi}_{hasta.hastaSoyadi}_{rapor_id}.pdf"'

    # Create PDF document
    p = canvas.Canvas(response)

    # Write report data to PDF
    y = 800  # Initial y-coordinate
    p.drawString(100, y, f"Rapor ID: {rapor.idRapor}")
    p.drawString(100, y - 20, f"Tarih: {rapor.raporTarihi}")


    # Get doctor details
    doktor = Doctor.objects.get(idDoctor=rapor.doktor_id)

    # Write doctor details to PDF
    p.drawString(100, y - 60, f"Doktor: {doktor.AD} {doktor.SOYAD}")
    p.drawString(100, y - 80, f"Hastane: {doktor.CalismaYeri}")
    p.drawString(100, y - 40, f"Polikinlik / Hastanın Başvurduğu Bölüm: {rapor.uzmanlikAlani}")

    # Write patient details to PDF
    p.drawString(100, y - 100, f"Hasta Adı-Soyadı: {hasta.hastaAdi} {hasta.hastaSoyadi}")
    p.drawString(100,y-120,f"Hasta ID'si:{hasta.idHasta}")

    p.drawString(100, y - 140, f"İçerik: {rapor.rapor_icerigi}")
    p.drawString(100, y - 160, f"Randevu ID: {rapor.randevunun_id}")

    p.save()
    return response

def rapor_duzenle_doctor(request, doktor_id):
    raporlar = TibbiRaporlar.objects.filter(doktor_id=doktor_id)
    return render(request, 'doktorun_yazdigi_raporlar.html', {'raporlar': raporlar})



def rapor_duzenle(request, rapor_id):
    rapor = get_object_or_404(TibbiRaporlar, idRapor=rapor_id)
    if request.method == 'POST':
        print(request.method)
        form = RaporForm(request.POST, instance=rapor)
        if form.is_valid():
            form.save()
            return redirect('rapor_duzenle_doctor', doktor_id=rapor.doktor_id)  # doktor_id'yi uygun şekilde temin ettiğinizden emin olun
    else:
        form = RaporForm(instance=rapor)
    return render(request, 'rapor_duzenle.html', {'form': form,'rapor':rapor})


def rapor_sil(request, idRapor):  # argüman adını rapor_id yerine idRapor olarak değiştirdik
    rapor = get_object_or_404(TibbiRaporlar, idRapor=idRapor)  # argümanı rapor_id yerine idRapor olarak değiştirdik
    doktor_id = rapor.doktor_id
    rapor.delete()
    return redirect('rapor_duzenle_doctor', doktor_id=doktor_id)
