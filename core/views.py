from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,'core/home.html')

def panel(request):
    return render(request,'core/panel.html')

def tienda(request):
    return render(request,'core/tienda.html')

def contacto(request):
    return render(request,'core/contacto.html')

def mascotas(request):
    return render(request,'core/mascotas.html')

def vacunas(request):
    return render(request,'core/vacunas.html')

def citas(request):
    return render(request,'core/citas.html')

def login_view(request):
    return render(request,'core/login.html')

def logout_view(request):
    return render(request,'core/logout.html')

def registro(request):
    return render(request,'core/registro.html')

def cita_crear(request):
    return render(request,'core/cita_crear.html')
