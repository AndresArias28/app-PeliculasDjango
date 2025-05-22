from django.contrib import admin
from django.urls import path
from appPeliculas import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio),
    path('agregarGenero/', views.agregarGenero),
    path('vistaAgregarGenero/', views.vistaAgregarGenero),
    path('listarPeliculas/', views.listarPeliculas, name='listar_peliculas'),
    path('agregarPelicula/', views.agregarPelicula),
    path('vistaAgregarPelicula/', views.vistaAgregarPelicula, name='agregar_pelicula'),
    path('consultarPeliculaPorId/<int:id>/', views.consultarPeliculaPorId),
    path('actualizaPelicula/', views.actualizarPelicula),
    path('eliminarPelicula/<int:id>/', views.eliminarPelicula),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)