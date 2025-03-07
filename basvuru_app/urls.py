from django.urls import path
from . import views


app_name = "basvuru_app"

urlpatterns = [
    path("yeni_basvuru" , views.yeni_basvuru , name="user_view"),
    path('admin_bekleyenler', views.admin_bekleyenler , name='admin_bekleyenler'),
    path('admin_onaylananlar' , views.admin_onaylananlar , name='admin_onaylananlar'),
    path("signup" , views.user_signup.as_view() , name= "user_signup"),
    path('basvurularim' , views.basvurularim , name='basvurularim'),
    path('giris' , views.login_control , name='login_control'),
    

    

]