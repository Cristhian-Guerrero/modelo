# Plataforma de Predicción de Carreras

Este proyecto es una aplicación web desarrollada en Django que utiliza Machine Learning para predecir las carreras más adecuadas para los estudiantes basándose en sus notas académicas. Además, permite comparar las predicciones de diferentes estudiantes y visualizar las predicciones en gráficos interactivos.

## Características

- **Predicción de carreras**: Los usuarios pueden ingresar las notas de un estudiante en diversas materias, y el modelo predictivo sugiere las carreras más adecuadas.
- **Comparación de predicciones**: Los usuarios pueden comparar las predicciones de varios estudiantes y visualizar las diferencias en gráficos interactivos.
- **Visualización de resultados**: Los resultados de las predicciones se muestran en gráficos de barras y gráficos de radar, destacando las carreras más probables y las materias con las notas más altas.

## Estructura del Proyecto

- **`predicciones/`**: Contiene el modelo Django con las vistas, modelos y URLs de la aplicación.
- **`templates/`**: Plantillas HTML utilizadas para las vistas.
  - **`base.html`**: Plantilla base que incluye el diseño general de la aplicación.
  - **`inicio.html`**: Página de inicio.
  - **`formulario.html`**: Formulario para ingresar las notas y realizar la predicción.
  - **`resultados.html`**: Muestra los resultados de la predicción en gráficos.
  - **`listar_predicciones.html`**: Lista todas las predicciones guardadas.
  - **`comparar_predicciones.html`**: Visualiza la comparación entre diferentes predicciones.
- **`modelo_entrenado.pkl`**: Archivo con el modelo de Machine Learning entrenado para las predicciones.

## Requisitos

- Python 3.7+
- Django 3.2+
- Librerías adicionales:
  - `pandas`
  - `joblib`
  - `matplotlib`
  - `seaborn`
  - `chart.js` (para gráficos en el frontend)

## Instalación y Configuración

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Cristhian-Guerrero/modelo.git
   cd tu-repositorio

Primero, debes crear y activar un entorno virtual. Para hacerlo, utiliza el siguiente comando:

```bash
python3 -m venv venv
so urce venv/bin/activate

Una vez que el entorno virtual esté activado, instala las dependencias necesarias con el comando:
```bash
pip install -r requirements.txt

Luego, configura la base de datos (por defecto se utiliza SQLite) ejecutando las migraciones:
```bash
python manage.py migrate

Después de configurar la base de datos, puedes iniciar el servidor local de Django con el siguiente comando:
```bash
python manage.py runserver

Una vez que el servidor esté en funcionamiento, podrás acceder a la aplicación desde tu navegador en la siguiente dirección:
```bash
Copiar código
http://127.0.0.1:8000/
Este conjunto de pasos te permitirá preparar el entorno, instalar las dependencias, configurar la base de datos, y ejecutar la aplicación Django en tu máquina local.
