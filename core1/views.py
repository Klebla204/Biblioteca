
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
from .models import CustomUser,Sede
from django.db.models import Sum
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm, LibroCreationForm

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
    total_libros = Libro.objects.count()
    total_usuarios = Sede.objects.count()
    total_prestamos = Prestamo.objects.count()

    context = {
        'total_libros': total_libros,
        'total_usuarios': total_usuarios,
        'total_prestamos': total_prestamos,
    }

    return render(request, 'biblioteca/index.html', context)
    
def catalog_view(request):
    query = request.GET.get('q', '')
    

    libros_qs = Libro.objects.select_related('sede')

    if query:
        libros_qs = libros_qs.filter(
            Q(titulo__icontains=query) |
            Q(autor__icontains=query) |
            Q(isbn__icontains=query) |
            Q(descripcion__icontains=query)
        )

    paginator = Paginator(libros_qs, 10)
    page_number = request.GET.get('page')
    libros = paginator.get_page(page_number)

    #new
    total_libros = Libro.objects.count()

    disponibles_ahora = (Libro.objects.aggregate(total=Sum('cant_disponible'))['total'] or 0)

    total_sedes = Sede.objects.count()


    return render(
        request,
        'catalogo/catalog.html',
        {
            'libros': libros,
            'query': query,
            'total_libros': total_libros,
            'disponibles_ahora': disponibles_ahora,
            'total_sedes': total_sedes,
        }
    )

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

def editar_usuarios(request,id):
    usuario=get_object_or_404(CustomUser,id=id)
    
    if request.method=='POST':
        form=CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('gestion_usuarios')
    else:
        form=CustomUserChangeForm(instance=usuario)
    return render(request,'menus/menu_admin/editar_usuario.html', {'form':form,'usuario':usuario})


def editar_libro(request, id):
    libro=get_object_or_404(Libro,id=id)
    if request.method=='POST':
        form=LibroCreationForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('gestion_libros')
    else:
        form=LibroCreationForm(instance=libro)
    return render(request,'menus/menu_admin/editar_libro.html', {'form':form,'libro':libro})

def eliminar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    libro.delete()
    return redirect('gestion_libros')

def mi_perfil(request):
    user=request.user
    role= request.user.role.strip().lower()
    if 'admin' in role:
        return render(request,'menus\menu_admin\menu_adminidtrador.html')
    elif 'biblio' in role:
        return render(request,'menus\menu_biblio\menu_bibliotecario.html')
    elif 'est' in role:
        return render(request,'menus\menu_estu\menu_estudiante.html')
    return '/'


def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_usuarios')
    else:
        form = CustomUserCreationForm()
    return render(request, 'menus/menu_admin/crear_usuario.html', {'form': form, 'accion': 'Crear'})



def eliminar_usuario(request, id):
    usuario = get_object_or_404(CustomUser, id=id)
    usuario.delete()
    return redirect('gestion_usuarios')

def crear_libro(request):
    if request.method== 'POST':
        form=LibroCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_libros')
    else:
        form= LibroCreationForm()
    return render(request,'menus/menu_admin/crear_libro.html', {'form': form, 'accion': 'Crear'})

def devolver_libro(request,id):
    libro= get_object_or_404(Prestamo, id=id)
    libro.finalizar()
    return redirect('gestion_prestamos')

    