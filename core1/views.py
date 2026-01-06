
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .models import Libro
from django.core.paginator import Paginator
from .models import Solicitud
from django.contrib.auth import logout


class CustomLoginView(LoginView):
   template_name= 'registration/Login.html'
   def get_success_url(self):
       user=self.request.user
       role= self.request.user.role.strip().lower()
       if 'admin' in role:
        return reverse('admin_menu')
       elif 'biblio' in role:
        return reverse('biblio_menu')
       elif 'est' in role:
        return reverse('est_menu')
       return '/'
       
def logout_view(request):
    logout(request)
    return redirect('catalog')   
    
def pagina_view(request):
    return render(request, 'biblioteca\index.html')
    
def catalog_view(request):
    libros_list= Libro.objects.filter(cant_disponible__gt=0)
    paginator= Paginator(libros_list, 10)
    page_number= request.GET.get('page')
    libros= paginator.get_page(page_number)
    return render(request,'catalogo\catalog.html', {'libros':libros})

def solicitar_prestamo(request, libro_id):
   libro= Libro.objects.get(id=libro_id)
   if libro.cant_disponible>0:
       libro.cant_disponible-=1
       libro.save()
       Solicitud.objects.create(
           estudiante=request.user,
           libro=libro,
           sede=libro.sede
       )
       return redirect('catalog')

def est_menu(request):
    return render(request,'menus\menu_estudiante.html')

def biblio_menu(request):
    return render(request,'menus\menu_bibliotecario.html')

def admin_menu(request):
    return render(request,'menus\menu_adminidtrador.html')

def solicitudes_pendientes(request):
    solicitudes= Solicitud.objects.filter(expirada=False, fecha_inicio_prestamo__isnull=True)
    for s in solicitudes:
        s.check_expiracion()
        return render(request, 'menus/listasolicitudes.html', {'solicitudes': solicitudes})



def redirect_after_login(request):
    user=request.user
    if user.role== 'admin':
        return redirect('admin_menu')
    elif user.role == 'bibliotecario':
        return redirect('biblio_menu')
    elif user.role == 'estudiante':
        return redirect('est_menu')
    else: return redirect('default_menu')