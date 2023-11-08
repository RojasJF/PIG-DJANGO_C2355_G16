from django import forms
from django.core.exceptions import ValidationError



class ContactoForm(forms.Form):
    nombre = forms.CharField(label="Nombre de contacto", required=True)
    apellido =forms.CharField(label="Apellido de contacto", widget=forms.TextInput(attrs={'class': 'fondo_rojo'}), required=True)
    edad = forms.IntegerField(label="Edad")
    mail = forms.EmailField(label="Mail", required=True)
    mensaje =  forms.CharField(widget=forms.Textarea)

    def clean_edad(self):
        if self.cleaned_data["edad"] < 18:
            raise ValidationError("El usuario no puede tener menos de 18 años")
        
        return self.cleaned_data["edad"]

    def clean(self):
        # Este if simula una busqueda en la base de datos
        if self.cleaned_data["nombre"] == "Carlos" and self.cleaned_data["apellido"] == "Lopez":
            raise ValidationError("El usuario Carlos Lopez ya existe")
        
        # Si el usuario no existe lo damos de alta

        return self.cleaned_data
    

class RegisterForm(forms.Form):
    nombre = forms.CharField(label="Nombre de contacto", required=True)
    apellido =forms.CharField(label="Apellido de contacto", required=True)
    DocIdN = forms.CharField(label="DNI", required=True,widget=forms.NumberInput,max_length=8)
    edad = forms.IntegerField(label="Edad")
    mail = forms.EmailField(label="Mail", required=True)
    Contraseña = forms.CharField(min_length=4,max_length=50,widget=forms.PasswordInput(),label="Contraseña         ")
    # Rcontraseña = forms.CharField(min_length=4,max_length=50,widget=forms.PasswordInput(),label="Repetir Contraseña")

    def clean_edad(self):
        if self.cleaned_data["edad"] < 18:
            raise ValidationError("El usuario no puede tener menos de 18 años")
        
        return self.cleaned_data["edad"]


        
    def clean(self):
        # Este if simula una busqueda en la base de datos
        if self.cleaned_data["DocIdN"] == "55555555":
            raise ValidationError("DNI registrado por favor verifique de nuevo")
        
        # Si el usuario no existe lo damos de alt
        return self.cleaned_data 