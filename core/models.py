from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

#------------------------------------
# Sucursal
#------------------------------------

class sucursal(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=120, blank=True)
    telefono = models.CharField(max_length=30, blank=True)

    class Meta:
         ordering =["nombre"]

    def __str__(self):
          return self.nombre
         

#---------------------------------------
# Usuario con rol propio
#---------------------------------------

class User(AbstractUser):
     ROLES =(
          ("ADMIN", "Administrador"),
          ("VET", "Veterinario"),
          ("REP", "Recepcionista"),
          ("OWNER", "Propietario"),
     )
     rol= models.CharField(max_length=20, choices=ROLES)

#------------------------------------------------
# Propietario
#------------------------------------------------

class propietario(models.Model):
     nombres = models.CharField(max_length=100)
     apellidos = models.CharField(max_length=100)
     cedula = models.CharField(max_length=16, unique=True, help_text="Formato: 000-000000-0000" )
     telefono = models.CharField(max_length=20)
     correo = models.EmailField(blank=True, null=True)
     direccion = models.TextField(blank=True, null=True)

     def __str__(self):
          return f"{self.nombres} {self.apellidos} - {self.cedula}"
     
#----------------------------------------------------------------
# Mascota(paciente)
#----------------------------------------------------------------

class Mascota(models.Model):
     ESPECIE_CHOISES = [
          ('CAN', 'Canino'),
          ('FEL', 'Felino'),
          ('AVE', 'Ave'),
          ('EXO', 'Exotico'),
          ('OTRO', 'otro'),
     ]

     nombre = (models.CharField(max_length=50))
     especie = models.CharField(max_length=10, choices= ESPECIE_CHOISES)
     raza = models.CharField(max_length=10, blank= True)
     fecha_nacimiento = models.DateField(null=True, blank=True)
     sexo = models.CharField(max_length=10, choices=[('M', 'Macho'), ('H', 'Hembra')])

     #------llave foranea que conecta con el propietario

     propietario = models.ForeignKey(propietario, on_delete = models.CASCADE, related_name='mascotas')

     def __str__(self):
          return f"{self.nombre} ({self.get_especie_display()}) - Dueño: {self.propietario.nombres}"



#-------------------------------------------------
# Servicios de la veterinaria
#-------------------------------------------------

class Servicio(models.Model):
     #Usamoa una tupla para que el usuario eliga uno de estos servicios
     TIPOS = (
          ('CONSULTA', 'Consulta General'),
          ('DESPARASITACION', 'Desparasitacion'),
          ('GROOMING', 'Grooming'),
          ('LABORATORIO', 'Laboratorio'),
          ('CIRUGIA', 'Cirugia Menor'),
          ('HOSPITALIZACION', 'Hospitalizacion'),
          ('HOSPEDAJE', 'Hospedaje'),
     )

     tipo = models.CharField(max_length=50, choices = TIPOS)
     descripcion = models.TextField(blank=True, null= True)
     precio= models.DecimalField(max_digits=10, decimal_places=2, help_text='precio en cordobas')
     sucursal= models.ForeignKey(sucursal, on_delete=models.CASCADE, related_name='servicios' )

     def __str__(self):
          return f"{self.get_tipo_display()} - {self.sucursal.nombre}"
     

#---------------------------------------------------------------------------
# Inventario farmacolofico 