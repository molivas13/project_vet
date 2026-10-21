from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import CitaForm, RegistroForm
from .models import Cita, Mascota


def home(request):
    return render(request, "core/home.html")


def tienda(request):
    productos = [
        {"nombre": "Alimentos premium perror 15kg", "precio": "C$1,250", "categoria": "comida"},
        {"nombre": "Alimento para gatos 10kg", "precio": "C$1,000", "categoria": "comida"},
        {"nombre": "Juguete para perro", "precio": "C$250", "categoria": "juguetes"},
        {"nombre": "Juguete para gato", "precio": "C$200", "categoria": "juguetes"},
        {"nombre": "Collar para perro", "precio": "C$150", "categoria": "accesorios"},
        {"nombre": "Collar para gato", "precio": "C$200", "categoria": "accesorios"},
    ]
    return render(request, "core/tienda.html", {"productos": productos})


def contacto(request):
    if request.method == "POST":
        messages.success(request, "¡Gracias! Hemos recibido tu mensaje y te contactaremos pronto")
        return redirect("core:contacto")
    return render(request, "core/contacto.html")


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f"¡Bienvenido/ a Petlovers, {usuario.username}!")
            return redirect("core:panel")
    else:
        form = RegistroForm()
    return render(request, "core/registro.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:panel")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("core:panel")
    else:
        form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("core:home")


def mascotas_del(usuario):
    return Mascota.objects.filter(propietario__correo__iexact=usuario.email)


def citas_del(usuario):
    return Cita.objects.filter(paciente__propietario__correo__iexact=usuario.email)


@login_required
def panel(request):
    proximas_citas = (
        citas_del(request.user)
        .filter(estado__in=["pendiente", "programada"])
        .order_by("fecha_solicitada", "fecha_hora")
    )
    contexto = {
        "total_mascotas": mascotas_del(request.user).count(),
        "total_vacunas": citas_del(request.user).filter(tipo="vacunacion").count(),
        "proximas_citas": proximas_citas[:5],
    }
    return render(request, "core/panel.html", contexto)


@login_required
def mascotas(request):
    contexto = {
        "mascotas": mascotas_del(request.user).select_related("propietario"),
    }
    return render(request, "core/mascotas.html", contexto)


@login_required
def vacunas(request):
    contexto = {
        "vacunas": citas_del(request.user)
        .filter(tipo="vacunacion")
        .select_related("paciente")
        .order_by("-fecha_solicitada"),
    }
    return render(request, "core/vacunas.html", contexto)


@login_required
def citas(request):
    contexto = {
        "citas": citas_del(request.user)
        .select_related("paciente", "sucursal", "veterinario")
        .order_by("fecha_solicitada", "fecha_hora"),
    }
    return render(request, "core/citas.html", contexto)


@login_required
def cita_crear(request):
    if request.method == "POST":
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            messages.success(request, f"Cita registrada para {cita.paciente.nombre}")
            return redirect("core:citas")
    else:
        form = CitaForm()
    return render(request, "core/cita_crear.html", {"form": form})
