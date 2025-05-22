from django.db import models

class Genero(models.Model):
    genNombre = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.genNombre
    


    
class Pelicula(models.Model):
    pelCodigo = models.CharField(max_length=10, unique=True)
    pelTitulo = models.CharField(max_length=100)
    pelProtagonista = models.CharField(max_length=100)
    pelDuracion = models.IntegerField(verbose_name="Duración en minutos")
    pelResumen = models.CharField(max_length=2000)
    pelFoto = models.ImageField(upload_to="fotos/", null=True, blank=True)
    pelEstado = models.BooleanField(default=True)
    pelGenero = models.ForeignKey(Genero, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.pelTitulo
    

