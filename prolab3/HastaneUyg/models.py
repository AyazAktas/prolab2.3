from django.db import models

# Create your models here.
class Doctor(models.Model):
    idDoctor = models.BigIntegerField("Doktor ID'si",default='',blank=True,primary_key=True)
    AD=models.TextField("Adı:",max_length=100,default='',blank=True)
    SOYAD=models.TextField("Soyadı:",max_length=100,default='',blank=True)
    UzmanlikAlani=models.TextField('Uzmanlık Alanı', max_length=120, default='', blank=True, null=True)
    CalismaYeri=models.TextField('Çalıştığı Hastane', max_length=120, default='', blank=True, null=True)

    class Meta:
        db_table = 'doktorlar'

class Hasta(models.Model):
    idHasta=models.IntegerField(blank=True,null=True)
    hastaAdi=models.CharField('Hasta Adı',max_length=120,default='',blank=True,null=True)
    hastaSoyadi=models.CharField('Hasta Soyadı',max_length=120,default='',blank=True,null=True)
    dogumTarihi=models.DateField("Doğum Tarihi",auto_now_add=False,auto_now=False,blank=True,null=True)
    cinsiyet=models.CharField('Cinsiyeti',max_length=1,default='',blank=True,null=False)
    telefonNo=models.TextField('Telefon Numarası',max_length=10,default='',blank=True,null=True)
    adres=models.TextField('Adres',max_length=3000,blank=False,null=False)
    class Meta:
        db_table = 'hastalar'


class Randevu(models.Model):
    randevuId = models.AutoField(primary_key=True)
    randevuTarihi = models.DateField("Randevu Tarihi", auto_now_add=False, auto_now=False, blank=True, null=True)
    randevu_saati = models.CharField("Randevu Saati", max_length=45, blank=True, null=True)
    doktor_id = models.IntegerField()  # Doktorun ID'sini tutacak sütun
    hasta_id = models.IntegerField()  # Hasta ID'sini tutacak sütun

    class Meta:
        db_table = 'randevular'
class TibbiRaporlar(models.Model):
    idRapor = models.AutoField(primary_key=True)
    raporTarihi = models.DateField(null=True)
    uzmanlikAlani = models.TextField(null=True)
    hasta_id = models.IntegerField()
    doktor_id = models.IntegerField()
    rapor_icerigi = models.TextField(null=True)
    randevunun_id = models.IntegerField()
    class Meta:
        db_table = 'tibbiraporlar'
class Yonetici(models.Model):
    idYonetici=models.IntegerField(blank=True,null=True)
    class Meta:
        db_table = 'yonetici'




