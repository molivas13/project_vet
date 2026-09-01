from django.urls import path 
from django.contrib.auth import views as auth_views


from . import views

app_name = "core"

urlpatterns = [
    path('', views.home, name='home'),
    path('panel/', views.panel, name='panel'),
    path('tienda/', views.tienda, name='tienda'),
    path('contacto/', views.contacto, name='contacto'),
    
    path('mascotas/', views.mascotas, name='mascotas'),
    path('vacunas/', views.vacunas, name='vacunas'),
    path('citas/', views.citas, name='citas'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('citas/nueva/', views.cita_crear,name='cita_crear'),
    
]