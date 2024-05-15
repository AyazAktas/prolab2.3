
from django import forms
from .models import Doctor,Hasta,Randevu,TibbiRaporlar

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['idDoctor', 'AD', 'SOYAD', 'UzmanlikAlani', 'CalismaYeri']
        widgets = {
            'idDoctor': forms.TextInput(attrs={'style': 'width: 50px;'}),  # Örneğin, idDoctor için genişliği 50 piksel olarak belirledik
            'AD': forms.TextInput(attrs={'style': 'width: 200px;'}),  # Örneğin, AD için genişliği 200 piksel olarak belirledik
            'SOYAD': forms.TextInput(attrs={'style': 'width: 200px;'}),  # Örneğin, SOYAD için genişliği 200 piksel olarak belirledik
            'UzmanlikAlani': forms.TextInput(attrs={'style': 'width: 200px;'}),  # Örneğin, UzmanlikAlani için genişliği 200 piksel olarak belirledik
            'CalismaYeri': forms.TextInput(attrs={'style': 'width: 200px;'}),  # Örneğin, CalismaYeri için genişliği 200 piksel olarak belirledik
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model=Hasta
        fields=['idHasta','hastaAdi','hastaSoyadi','dogumTarihi','cinsiyet','telefonNo','adres']
        widgets = {
            'dogumTarihi': forms.DateInput(attrs={'type': 'date'}),
            'cinsiyet': forms.TextInput(attrs={'style': 'width: 50px' , 'size':'1'}),
            'telefonNo': forms.TextInput(attrs={'size': '10'})
        }


class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model=Hasta
        fields=['idHasta','hastaAdi','hastaSoyadi','dogumTarihi','cinsiyet','telefonNo','adres']
        widgets = {
            'dogumTarihi': forms.DateInput(attrs={'type': 'date'}),
            'cinsiyet': forms.TextInput(attrs={'style': 'width: 50px' , 'size':'1'}),
            'telefonNo': forms.TextInput(attrs={'size': '10'})
        }


class RandevuForm(forms.ModelForm):
    class Meta:
        model = Randevu
        fields = ['randevuTarihi', 'randevu_saati', 'hasta_id', 'doktor_id']


class RaporForm(forms.ModelForm):
    class Meta:
        model = TibbiRaporlar
        fields = ['hasta_id', 'doktor_id', 'raporTarihi', 'rapor_icerigi', 'uzmanlikAlani', 'randevunun_id']
        widgets = {
            'raporTarihi': forms.DateInput(attrs={'type': 'date'})
        }