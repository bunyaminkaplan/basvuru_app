from django.db import models

# Create your models here.

class basvuru_details (models.Model) :

    basvuru_sahibi = models.CharField(max_length=30, default= 'none')
    pasaport_turu = models.CharField(max_length=30)
    tc_no = models.IntegerField()
    isim_soyisim = models.CharField(max_length=30)
    kadro_unvani = models.CharField(max_length=30)
    kurum_sicil_no = models.IntegerField()
    tel_no = models.IntegerField()
    email = models.EmailField(max_length=40)
    nufus_mudurluk = models.CharField(max_length=40)
    cocuk_sayisi = models.IntegerField()
    gerekce = models.CharField(max_length=50 , null=True)
    onay = models.BooleanField(default=False)
    
