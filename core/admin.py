from django.contrib import admin
from .models import User, sucursal, Servicio, propietario, Mascota
# Register your models here.
admin.site.register(propietario)
admin.site.register(Mascota)
