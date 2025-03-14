from django.shortcuts import render
from django.shortcuts import render , redirect
from basvuru_app import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import urls
from django.views.generic import CreateView
from django.urls import reverse , reverse_lazy
from django.contrib.auth import logout
import requests
from bs4 import BeautifulSoup

import time

def yeni_basvuru (request):
    
    try:
        if is_logged_in:
            if request.method == "POST":

                pasaport_turu = request.POST.get("pasaport_turu")
                tc_no = request.POST.get('tc_no')
                isim_soyisim = request.POST.get('isim_soyisim')
                kadro_unvani = request.POST.get('kadro_unvani')
                kurum_sicil_no = request.POST.get('kurum_sicil_no')
                tel_no = request.POST.get('tel_no')
                email = request.POST.get('mail')
                nufus_mudurluk = request.POST.get('nufus_mudurlugu')
                cocuk_sayisi = request.POST.get('cocuk_sayisi')
                
                temp_model = models.basvuru_details(
                    pasaport_turu = pasaport_turu , 
                    tc_no = tc_no , 
                    isim_soyisim = isim_soyisim,
                    kadro_unvani = kadro_unvani, 
                    kurum_sicil_no = kurum_sicil_no,
                    tel_no = tel_no,
                    email = email,
                    nufus_mudurluk = nufus_mudurluk,
                    cocuk_sayisi = cocuk_sayisi,
                    basvuru_sahibi = current_username
                    )
                temp_model.save()
                
            return render(request, 'basvuru_app/yeni_basvuru.html')
        else:
            return redirect(reverse('basvuru_app:login_control'))
        
    except NameError:
        return redirect(reverse('basvuru_app:login_control'))

def admin_bekleyenler (request):
    try:
        if is_logged_in and is_current_user_staff:
            if request.method == 'POST':
                basvuru_id = request.POST.get('id')
                guncel_basvuru = models.basvuru_details.objects.get(id = basvuru_id)
                if 'red' in request.POST:
                    gerekce = request.POST.get('gerekce')
                    if gerekce:
                        guncel_basvuru.gerekce = gerekce
                        guncel_basvuru.onay = False
                        guncel_basvuru.save()
                        print('red worked')

                elif 'onay' in request.POST:
                    guncel_basvuru.onay = True
                    guncel_basvuru.gerekce = None
                    guncel_basvuru.save()
                    print('onay worked')
        else:
            return redirect(reverse('basvuru_app:login_control'))
    except NameError:
        return redirect(reverse('basvuru_app:login_control'))
        

    basvurular = models.basvuru_details.objects.filter( onay = False).all()
    return render(request , 'basvuru_app/admin_bekleyenler.html' , context={'basvurular' : basvurular})

def admin_onaylananlar (request):
    try:
        if is_logged_in and is_current_user_staff:
            basvurular = models.basvuru_details.objects.filter(onay = True).all()
            return render(request , 'basvuru_app/admin_onaylananlar.html' , context= {'basvurular' : basvurular})
        else: 
            return redirect(reverse('basvuru_app:login_control'))
    except NameError:
        return redirect(reverse('basvuru_app:login_control'))
    
def basvurularim(request):
    try:
        if is_logged_in:
            basvurular = models.basvuru_details.objects.filter(basvuru_sahibi = current_username).all()
            
            return render( request , 'basvuru_app/basvurularim.html' , context={'basvurular': basvurular})
        else:
            return redirect(reverse('basvuru_app:login_control'))
    except NameError:
        return redirect(reverse('basvuru_app:login_control'))

class user_signup(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('basvuru_app:login_control')
    template_name = "registration/signup.html"

def user_logout (request):
    global is_logged_in
    is_logged_in = False
    print('logged info' ,is_logged_in)
    logout(request)

def login_control(request):
    if request.method == 'POST':
        session = requests.Session()
        form_url = "http://127.0.0.1:8000/giris"
        response = session.get(form_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
        # print(csrf_token)
        global current_username
        current_username = request.POST.get('username')
        pw = request.POST.get('password')
        url = "http://127.0.0.1:8000/login/"
        form = {
            'csrfmiddlewaretoken' : csrf_token,
            'id_username' : str(current_username) ,
            'id_password' : str(pw)
        }
        
        response = session.post(url, data=form)
        if response.status_code == 200:
            
            global is_logged_in 
            is_logged_in = True
            print('logged info' ,is_logged_in)
            global is_current_user_staff
            is_current_user_staff = User.objects.get(username = current_username).is_staff
            if is_current_user_staff:

                print('staff')
                return redirect(reverse("basvuru_app:admin_bekleyenler"))   
            else:

                print('not staff')
                return redirect(reverse("basvuru_app:basvurularim"))
        else:
            re = response.text
            # print(re)

    return render(request , template_name='registration/giris.html')    