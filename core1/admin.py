from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.forms import  UserCreationForm, UserChangeForm
from .models import Libro, Sede

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form= UserCreationForm
    form= UserChangeForm
    model= CustomUser
    list_display=('username', 'email', 'role', 'is_staff','is_superuser')
    add_fieldsets= ((None, {'classes':('wide'), 'fields':('username', 'password1', 'password2','role'),}),)
    fieldsets= UserAdmin.fieldsets + (('Rol', {'fields':('role',)}),
                                      )

class LibroAdmin(admin.ModelAdmin):
    list_display=('titulo', 'autor', 'cantidad disponible', 'categoria','sede')
    search_fields=('titulo', 'autor','isbn')
    list_filter=('categoria')

class SedeAdmin(admin.ModelAdmin):
    list_display=('nombre', 'telefono')



admin.site.register(CustomUser)
admin.site.register(Libro)
admin.site.register(Sede)