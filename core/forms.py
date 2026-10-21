from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Cita, User


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.rol = "OWNER"
        if commit:
            usuario.save()
        return usuario


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ["paciente", "veterinario", "sucursal", "fecha_hora", "tipo", "notas"]
        widgets = {
            "fecha_hora": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notas": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["veterinario"].queryset = User.objects.filter(rol="VET")
