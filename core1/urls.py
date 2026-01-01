from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.pagina_view, name='index'),
    path('pagina/',views.pagina_view, name='pagina'),
    path('login/', auth_views.LoginView.as_view(template_name="registration/Login.html"), name='Login'),
    path('catalog/',views.catalog_view, name='catalog'),
]
