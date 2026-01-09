from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import redirect_after_login, prestamos_activos, reserva_activa, gestion_prestamos
from .views import CustomLoginView, admin_menu, biblio_menu, est_menu, gestion_libros,reportes_view
from .views import solicitar_prestamo, logout_view, solicitudes_pendientes, aceptar_solicitud, gestion_usuarios
urlpatterns = [
    path('', views.pagina_view, name='index'),
    path('pagina/',views.pagina_view, name='pagina'),
    path('catalog/',views.catalog_view, name='catalog'),
    path('redirect-after-login', redirect_after_login,name='redirect_after_login'),
    path('menu/estudiante/', est_menu, name='est_menu'),
    path('menu/bibliotecario/',biblio_menu, name='biblio_menu'),
    path('menu/admin',admin_menu, name='admin_menu'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('solicitar/<int:libro_id>/', solicitar_prestamo, name='solicitar_prestamo'),
    path('logout/',logout_view, name='logout_view'),
    path('lista_solicitudes/', solicitudes_pendientes, name='solicitudes_pendientes' ),
    path('aceptar_solicitud/<int:solicitud_id>/', aceptar_solicitud,name='aceptar_solicitud'),
    path('gestion_usuarios/', gestion_usuarios, name='gestion_usuarios'),
    path('prestamos_activos/', prestamos_activos, name='prestamos_activos' ),
    path('reserva_activa/', reserva_activa, name='reserva_activa'),
    path('gestion_prestamos/', gestion_prestamos,name='gestion_prestamos'),
    path('gestion_libros/', gestion_libros, name='gestion_libros'),
    path('reportes_view/', reportes_view, name='reportes_view'),
    ]
