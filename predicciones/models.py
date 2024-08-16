from django.db import models

class Prediccion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    estudiante = models.CharField(max_length=100)
    anio = models.IntegerField()  # Nuevo campo para año
    periodo = models.IntegerField()  # Nuevo campo para periodo
    resultados = models.JSONField()

    def __str__(self):
        return f"Predicción de {self.estudiante} en {self.fecha} - Año {self.anio}, Periodo {self.periodo}"
