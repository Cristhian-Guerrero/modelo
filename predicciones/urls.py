from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('predecir/', views.predecir, name='predecir'),
    path('comparar/', views.comparar_predicciones, name='comparar_predicciones'), 
    path('listar/', views.listar_predicciones, name='listar_predicciones'),
    path('eliminar/<int:id>/', views.eliminar_prediccion, name='eliminar_prediccion'),
    path('modificar/<int:id>/', views.modificar_prediccion, name='modificar_prediccion'),
    path('visualizar/<int:id>/', views.visualizar_prediccion, name='visualizar_prediccion'),  # Nueva ruta
]
