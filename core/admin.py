from django.contrib import admin
from django. contrib.auth.admin import UserAdmin
from .models import User, Sucursal, Servicio, Propietario, Mascota, Farmaco, CitaFarmaco,Cita
# Register your models here.

#--------------------------------------------
#1. USUARIOS Y SUCURSALES
#--------------------------------------------
@admin.register(User)
class CustomUserAdmin(UserAdmin): 
    fieldsets = UserAdmin.fieldsets +(
        ('Informacion Adicional', {'fields' : ('rol', 'telefono')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', )
    list_filter = ('rol', 'is_staff', 'is_active')

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion','ciudad','telefono')
    search_fields = ('nombre',)

#--------------------------------------------------------------
# 2. CLIENTES Y PACIENTES
#--------------------------------------------------------------

@admin.register(Propietario)
class PropietarioAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'cedula', 'telefono')
    search_fields = ('nombres', 'apellidos', 'cedula')

@admin.register(Mascota)
class MascotaAdminin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'sexo', 'propietario')
    search_fields = ('nombre','propietario_nombres','propietario__apellidos')



    
#--------------------------------------------------------
# INVENTARIO FARMACOLOGICO 
#---------------------------------------------------------

@admin.register(Farmaco)
class FarmacoAdmin(admin.ModelAdmin):
    list_display = ('nombre','categoria','stock','Sucursal','actualizado')
    list_filter = ('categoria', 'Sucursal')
    search_fields = ('nombre',)
    readonly_fields = ('creado', 'actualizado',)

#----------------------------------------------------------
# CITAS Y ATENCION MEDICA (CON INLINES
#----------------------------------------------------------
# esto permite agregar los farmacos directamente dentro de la pantalla
class CitaFarmacoInline(admin.TabularInline):
    model = CitaFarmaco
    extra = 1 

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente','tipo', 'fecha_solicitada', 'estado', 'veterinario','sucursal')
    list_filter = ('estado', 'tipo', 'sucursal', 'fecha_solicitada')
    search_fields = ('paciente__nombre', 'veterinario__username')
    inlines = [CitaFarmacoInline] #conectamos la tabla directamente
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('tipo','descripcion','precio','sucursal')
    list_filter = ('tipo','sucursal', 'descripcion')
    

#--------------------------------------------------------------
# CONTROL PREVENTIVO
# -------------------------------------------------------------
