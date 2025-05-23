from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import Error
from appPeliculas.models import Pelicula, Genero
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from django.shortcuts import render
from .models import Pelicula, Genero
from django.db import DatabaseError  


def inicio(request):
    return render(request, 'inicio.html')

@csrf_exempt # quitar la respuesta csrf
def agregarGenero(request):
    try:
        nombre = request.POST['txtNombre']
        if not nombre:
            return JsonResponse({'error': 'El nombre del género es requerido.'}, status=400)

        genero = Genero(genNombre=nombre)
        genero.save()
        mensaje = 'Genero agregado correctamente'
        status_code = 200
    except Error as e:
        mensaje = str(e)
        status_code = 500
        

    peliculas = list(Pelicula.objects.values())
    contexto = {
        'mensaje': mensaje,
        'peliculas': peliculas,
    }
    ## return JsonResponse(contexto)
    return render(request, 'listarPeliculas.html', contexto)

def vistaAgregarGenero(request):
    return render(request, 'agregarGenero.html')

#@csrf_exempt
def listarPeliculas(request):
    peliculas = Pelicula.objects.all()
    # Convertir queryset a lista de diccionarios
    peliculas = list(peliculas.values())
    print(peliculas)
    retorno = {'peliculas': peliculas}
    #return JsonResponse(retorno, safe=False) 
    return render(request, 'listarPeliculas.html', retorno)

# @csrf_exempt
def agregarPelicula(request):
    message = ''
    pelicula = None
    try:
        codigo = request.POST['txtcodigo']
        titulo = request.POST['txttitulo']
        protagonista = request.POST['txtprotagonista']
        duracion = int(request.POST['txtDuracion'])
        resumen = request.POST['txtresumen']
        foto = request.FILES['txtfoto']
        id_genero = int(request.POST['txtgenero'])

        genero = Genero.objects.get(pk=id_genero)

        # crear el objeto Pelicula
        pelicula = Pelicula(
            pelCodigo=codigo,
            pelTitulo=titulo,
            pelDuracion=duracion,
            pelProtagonista=protagonista,
            pelResumen=resumen,
            pelFoto=foto,
            pelGenero=genero
        )

        pelicula.save()
        message = 'Película agregada correctamente'

    except Genero.DoesNotExist:
        message = 'Género no encontrado.'
    except (ValueError, KeyError) as e:
        message = f'Error en los datos ingresados: {e}'
    except DatabaseError as e:
        message = f'Error de base de datos: {e}'
    except Exception as e:
        message = f'Ocurrió un error inesperado: {e}'

    peliculas = Pelicula.objects.all()

    contexto = {
        'message': message,
        'peliculas': peliculas,
    }

    if pelicula:
        contexto['idPelicula'] = pelicula.id

    # return render(request, 'listarPeliculas.html', contexto)
    return JsonResponse({'message': message, 'pelicula': pelicula.id}, status=200)


def vistaAgregarPelicula(request):
    generos = Genero.objects.all()
    retorno = {'generos': generos}
    return render(request, 'agregarPelicula.html', retorno)

def consultarPeliculaPorId(request, id):
    try:
        pelicula = Pelicula.objects.get(pk=id)
        generos = Genero.objects.all()
        retorno = {
            'pelicula': pelicula,
            'generos': generos
        }
        return render(request, 'modificarPelicula.html', retorno)
    except Pelicula.DoesNotExist:
        retorno = {'mensaje': 'Pelicula no encontrada'}
        return render(request, 'modificarPelicula.html', retorno)
    except Error as e:
        retorno = {'mensaje': str(e)}
        return render(request, 'modificarPelicula.html', retorno)

# @csrf_exempt    
def actualizarPelicula(request):
    try:
        id = request.POST['idPelicula']
        peliculaActualizar = Pelicula.objects.get(pk=id)  # Obtener la película a actualizar
        
        peliculaActualizar.pelCodigo = request.POST['txtcodigo']
        peliculaActualizar.pelTitulo = request.POST['txttitulo']
        peliculaActualizar.pelDuracion = int(request.POST['txtDuracion'])
        peliculaActualizar.pelProtagonista = request.POST['txtprotagonista']
        peliculaActualizar.pelResumen = request.POST['txtresumen']
        
        idGenero = int(request.POST['txtgenero'])  # Obtener el ID del género
        genero = Genero.objects.get(pk=idGenero) # Obtener el objeto Genero
        peliculaActualizar.pelGenero = genero
        
        foto = request.FILES.get('txtfoto')  # Cambiado a get para evitar KeyError
        if foto:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(peliculaActualizar.pelFoto)))
            peliculaActualizar.pelFoto = foto

        peliculaActualizar.save()
        
        peliculas = list(Pelicula.objects.values())
        contexto = {
            'mensaje': 'Película actualizada correctamente',
            'peliculas': peliculas,
            'idPelicula': peliculaActualizar.id
        }
        # return JsonResponse( contexto, status=200)
        
        return render(request, 'listarPeliculas.html', contexto)
        
        mensaje = 'Película actualizada correctamente'
    except Genero.DoesNotExist:
        mensaje = 'Género no encontrado.'
    except Pelicula.DoesNotExist:
        mensaje = 'Película no encontrada.'
    except (ValueError, KeyError) as e:
        mensaje = f'Error en los datos ingresados: {e}'
    except DatabaseError as e:
        mensaje = f'Error de base de datos: {e}'
    except Exception as e:
        mensaje = f'Ocurrió un error inesperado: {e}'

    peliculas = list(Pelicula.objects.values())

    contexto = {
        'mensaje': mensaje,
        'peliculas': peliculas,
    }

    return JsonResponse(contexto, status=400)


def eliminarPelicula(request, id):
    try:
        pelicula = Pelicula.objects.get(pk=id)
        os.remove(os.path.join(settings.MEDIA_ROOT, str(pelicula.pelFoto)))
        pelicula.delete()
        mensaje = 'Película eliminada correctamente'
    except Pelicula.DoesNotExist:
        mensaje = 'Película no encontrada'
    except Error as e:
        mensaje = str(e)
        
    peliculas = Pelicula.objects.all()
    retorno = {'mensaje': mensaje, 'peliculas': peliculas}
    return render(request, 'listarPeliculas.html', retorno)