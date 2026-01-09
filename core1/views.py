
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .models import Libro
from django.core.paginator import Paginator
from .models import Solicitud, Prestamo
from django.contrib.auth import logout
from datetime import timedelta
from django.utils import timezone
from .models import CustomUser

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
    return render(request,'menus\menu_estu\menu_estudiante.html')

def biblio_menu(request):
    return render(request,'menus\menu_biblio\menu_bibliotecario.html')

def admin_menu(request):
    return render(request,'menus\menu_admin\menu_adminidtrador.html')

def solicitudes_pendientes(request):
    solicitudes= Solicitud.objects.filter(expirada=False)
    for s in solicitudes:
        s.check_expiracion()
        return render(request, 'menus\menu_biblio\solicitudes_prestamos.html', {'solicitudes': solicitudes})

def aceptar_solicitud(request, solicitud_id):
    solicitud= Solicitud.objects.get(id=solicitud_id)
    prestamo= Prestamo.objects.create(
        estudiante= solicitud.estudiante,
        libro= solicitud.libro,
        sede= solicitud.sede,
        fecha_inicio=timezone.now().date(),
        fecha_fin=timezone.now().date()+ timedelta(days=35)
    )
    solicitud.expirada=True
    solicitud.save()
    return redirect('solicitudes_pendientes')

    
    
    

def redirect_after_login(request):
    user=request.user
    if user.role== 'admin':
        return redirect('admin_menu')
    elif user.role == 'bibliotecario':
        return redirect('biblio_menu')
    elif user.role == 'estudiante':
        return redirect('est_menu')
    else: return redirect('default_menu')


def gestion_usuarios(request):
    usuarios= CustomUser.objects.all()
    return render(request, 'menus\menu_admin\gestion_usuarios.html', {'usuarios':usuarios})

def prestamos_activos(request):
    usuario= request.user
    prestamos= Prestamo.objects.filter(estudiante = usuario)
    return render(request,'menus\menu_estu\prestamos_estudiante.html', {'prestamos': prestamos} )


def reserva_activa(request):
    usuario= request.user
    reservas = Solicitud.objects.filter(estudiante= usuario)
    return render(request, 'menus\menu_estu\mis_reservas.html', {'reservas': reservas})

def gestion_prestamos(request):
    prestamos= Prestamo.objects.filter(activo=True)
    return render(request, 'menus\menu_biblio\gestion_prestamos.html', {'prestamos': prestamos})

def gestion_libros(request):
    libros = Libro.objects.all()
    return render(request, 'menus\menu_admin\gestion_libros.html', {'libros':libros})

def reportes_view(request):
    return render(request, 'menus/menu_admin/reportes.html')

    