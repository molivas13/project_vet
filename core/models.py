from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone


# Create your models here.

#------------------------------------
# Sucursal
#------------------------------------

class Sucursal(models.Model):
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
#---------------------------------------------------------------------------
#Especie
#----------------------------------------------------------------------------
#class Especie(models.Model):
#    nombre = models.CharField(max_length=50, unique=True)

#    def __str__(self):
#          return self.nombre
#

#------------------------------------------------
# Propietario
#------------------------------------------------

class Propietario(models.Model):
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

     propietario = models.ForeignKey('Propietario', on_delete = models.CASCADE, related_name='mascotas')

     def __str__(self):
          return f"{self.nombre} ({self.get_especie_display()}) - Dueño: {self.propietario.nombres}"
#---------------------------------------------------------------------------
# Inventario farmacologico
#---------------------------------------------------------------------------
     
class Farmaco(models.Model):
     class Categoria(models.TextChoices):
          ANALGESICOS_ANTIFLAMATORIOS = (
               "analgesicos_antiflamatorios", 
               "Analgesicos y antiflamatorios",
          )

          ANTIBOTICOS = ("antibioticos", "Antibioticos")
          ANTIPARARASITARIOS_INTERNOS = (
               "antiparasitarios_internos",
               "Antiparasitarios externos",
          )
          VACUNAS = ("vacunas", "Vacunas")
          ANTIEMETICOS_DIGESTIVOS = (
               "antiemeticos_digestivos",
               "Antiemeticos y digestivos",
          )
          SUEROS_SOLUCIONES = (
               "sueros_soluciones",
               "sueros y soluciones",
          )
          ANTICONVULSIVOS =("anticonvulsivos", "Anticonvulsivos")
          CORTICOIDES = ("corticoides", "Corticoides")
          ANESTESICOS_SEDANTES = (
               "anestesicos_sedantes",
               "Anestesicos y sedantes",
          )
          ANTISEPTICOS_TOPICOS = (
               "antisepticos_topicos",
               "Antisepticos y topicos",
          )
          HOROMONAS_ENDOCRINOS =(
               "hormonas_endocrinos",
               "hormonas y tratamientos endocrinos",
          )
          OFTALMICOS_OTICOS = (
               "oftalmicos_oticos",
               "oftalmicos y oticos"
          )
          PRODUCTOS_DERMATOLOGICOS =(
               "productos_dermatologicos",
               "productos dermatologicos"
          )
          EUTANACIA_EMERGENCIA =(
               "eutanasia_emergencias",
               "Eutanasia y emergencias",
          )

     Sucursal =models.ForeignKey(
          'Sucursal',
          on_delete=models.PROTECT,
          related_name="farmacos",
     )

     nombre = models.CharField(max_length=150)
     categoria = models.CharField(
          max_length=60,
          choices=Categoria.choices,
     )
     descripcion = models.TextField()
     stock = models.PositiveBigIntegerField(default=0)
     creado = models.DateTimeField(auto_now_add=True)
     actualizado = models.DateTimeField(auto_now=True)

     class Meta:
          ordering = ["Sucursal__nombre", "categoria", "nombre"]
          unique_together = ("Sucursal", "nombre")

     def __str__(self):
          return f"{self.nombre} - {self.sucursal.nombre}"

#-----------------------------------------------------------------
# cita famarco
#-----------------------------------------------------------------

class CitaFarmaco(models.Model):
     cita = models.ForeignKey(
          "Cita",
          on_delete=models.CASCADE,
          related_name= "administraciones_farmacos",
     )
     farmaco = models.ForeignKey(
          "Farmaco",
          on_delete= models.PROTECT,
          related_name= "administraciones",
     )
     cantidad = models.PositiveIntegerField(default= 1)
     registrado = models.DateTimeField(auto_now_add=True)

     class Meta:
          ordering =["farmaco__nombre"]
          unique_together = ("cita", "farmaco")

     def __str__(self):
          return f"Cita de {self.cita_id} - {self.farmaco.nombre} ({self.cantidad})"       

#---------------------------------------------------------------------------
# Cita 
#---------------------------------------------------------------------------

class Cita(models.Model):
     ESTADOS = (
          ("pendiente", "Pendiente"),
          ("programada", "Programada"),
          ("atendida", "Atendida"),
          ("cancelada", "cancelada"),     
     )
     TIPOS = (
          ("consulta", "Consulta"),
          ("vacunacion", "Vacunacion"),
          ("cancelada", "Cancelada"),
          ("cirugia", "Cirugia"),
     )
     paciente = models.ForeignKey('Mascota', on_delete=models.CASCADE)
     veterinario = models.ForeignKey(
          'User',
          limit_choices_to={"rol": "VET"},
          on_delete=models.PROTECT,
          related_name="citas",
     )
     sucursal = models.ForeignKey(
          'Sucursal',
          on_delete=models.PROTECT,
          related_name="citas",     
     )
     fecha_solicitada = models.DateField(default=timezone.now)
     fecha_hora = models.DateTimeField(blank=True, null=True)
     duracion = models.IntegerField(default=30)
     tipo = models.CharField(max_length=50, choices=TIPOS, default="consulta")
     estado = models.CharField( max_length=20, choices=ESTADOS, default = "pendiente")
     notas = models.TextField(blank=True)
     farmacos_utilizados = models.ManyToManyField(
          "Farmaco",
          blank=True,
          related_name="citas_utilizadas",
          through= "CitaFarmaco",
          through_fields=("cita","farmaco"),
          help_text="Medicamentos del inventario utilizados durante la atencion.",
     )
     def __str__(self):
        # 1. Definimos nombres básicos (corregido 'username')
        vet_nombre = self.veterinario.username if self.veterinario else "Sin asignar"
        suc_nombre = self.sucursal.nombre if self.sucursal else "Sin sucursal"

        # 2. Lógica de fecha (corregido el if/else en una sola línea)
        if self.fecha_hora:
            fecha_local = timezone.localtime(self.fecha_hora) if timezone.is_aware(self.fecha_hora) else self.fecha_hora
            fecha_texto = fecha_local.strftime("%d/%m/%Y %H:%M")
        else:
            fecha_texto = f"{self.fecha_solicitada.strftime('%d/%m/%Y')} (sin horario)"
        
        # 3. Retorno (corregido 'sucurcal_nombre' y concatenación)
        return f"Cita: {self.paciente.nombre} ({self.get_estado_display()}) en {suc_nombre} con {vet_nombre} - {fecha_texto}"

     def telefono_contacto(self) -> str:
        try:
            propietario = self.paciente.propietario
            telefono = propietario.telefono if propietario.telefono else ""
            return "".join(ch for ch in telefono if ch.isdigit())
        except AttributeError:
            return ""

     def mensaje_whatsapp(self) -> str:
        propietario = self.paciente.propietario
        nombre_propietario = f"{propietario.nombres} {propietario.apellidos}"
        fecha = self.fecha_solicitada.strftime("%d/%m/%Y")
        
        return (
            f"Hola {nombre_propietario}, te saludamos de Pet Lovers. "
            f"¿Podemos coordinar el horario para la cita de {self.paciente.nombre} del {fecha}?"
        )



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
     sucursal= models.ForeignKey('Sucursal', on_delete=models.CASCADE, related_name='servicios' )

     def __str__(self):
          return f"{self.get_tipo_display()} - {self.sucursal.nombre}"

 



     















