# forms.py
from django import forms
from .models import Doctor,Hasta,Randevu

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['idDoctor','AD', 'SOYAD', 'UzmanlikAlani', 'CalismaYeri']


class PatientForm(forms.ModelForm):
    class Meta:
        model=Hasta
        fields=['idHasta','hastaAdi','hastaSoyadi','dogumTarihi','cinsiyet','telefonNo','adres']
        widgets = {
            'dogumTarihi': forms.DateInput(attrs={'type': 'date'}),
            'telefonNo': forms.TextInput(attrs={'size': '10'})
        }


class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Hasta
        fields=['idHasta','hastaAdi','hastaSoyadi','dogumTarihi','cinsiyet','telefonNo','adres']
        widgets = {
            'dogumTarihi': forms.DateInput(attrs={'type': 'date'}),
            'telefonNo': forms.TextInput(attrs={'size': '10'})
        }

from django import forms
from .models import Randevu

class RandevuForm(forms.ModelForm):
    class Meta:
        model = Randevu
        fields = ['randevuTarihi', 'randevuSaati', 'idDoctor', 'idHasta']
