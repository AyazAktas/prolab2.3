"""
URL configuration for prolab3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from HastaneUyg import views


urlpatterns = [
    path('admin/login/', views.admin_login, name='admin_login'),  # admin/login/ URL'sini önce ekleyin
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('doctor/login/', views.doctor_login, name='doctor_login'),
    path('patient/login/', views.patient_login, name='patient_login'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('doctor/create/', views.doctor_create, name='doctor_create'),
    path('list_doctors/', views.list_doctors, name='list_doctors'),
    path('doctor/<int:doctor_id>/delete/', views.delete_doctor, name='delete_doctor'),
    path('patient/create/', views.patient_create, name='patient_create'),
    path('list_patients/', views.list_patients, name='list_patients'),
    path('patient/<int:hasta_id>/delete/', views.delete_patient, name='delete_patient'),
    path('patient/register/', views.patient_register, name='patient_register'),
    path('patient_page/<int:id>/', views.patient_page, name='patient_page'),
    path('patient_info/<int:hasta_id>/', views.patient_info, name='patient_info'),
    path('doctor_page/<int:doktor_id>/', views.doctor_page, name='doctor_page'),
    path('randevu_al/<int:hasta_id>/', views.randevu_al, name='randevu_al'),
    path('randevularim/<int:hasta_id>/', views.randevularim, name='randevularim'),
    path('randevu_sil/<int:randevu_id>/', views.randevu_sil, name='randevu_sil'),
    path('rapor_yazilabilir/<int:doktor_id>/', views.rapor_yazilabilir, name='rapor_yazilabilir'),
    path('rapor_yaz/<int:randevu_id>/', views.rapor_yaz, name='rapor_yaz'),
    path('raporlarim/<int:hasta_id>/', views.raporlarim, name='raporlarim'),
    path('raporlarim/pdf/<int:rapor_id>/', views.raporlarim_pdf, name='raporlarim_pdf'),
]
