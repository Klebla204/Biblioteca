from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,Libro

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model=CustomUser
        fields= ('username', 'email','role','password1','password2')
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model=CustomUser
        fields= ('username', 'email','role')
        

class LibroCreationForm(forms.ModelForm):
   class Meta:
       model=Libro
       fields=('titulo','autor','isbn','descripcion','cant_total','cant_disponible','fecha_publicacion','categoria','sede')
           