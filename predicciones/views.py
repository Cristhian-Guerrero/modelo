import seaborn as sns
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import matplotlib.pyplot as plt
import io
import urllib, base64
import joblib
import pandas as pd
import json  # Importar json para serializar los resultados
from .models import Prediccion

# Cargar el modelo entrenado
modelo = joblib.load('predicciones/modelo_entrenado.pkl')

# Mapeo de materias para facilitar el uso
materias = {
    'Matemáticas': 'matematicas',
    'Español': 'espanol',
    'Biología': 'biologia',
    'C-Sociales': 'c_sociales',
    'Inglés': 'ingles',
    'Edu-Física': 'edu_fisica',
    'Informática': 'informatica',
    'Artes': 'artes',
    'Religión': 'religion',
    'Filosofía': 'filosofia',
    'Economía': 'economia'
}

def inicio(request):
    return render(request, 'inicio.html')

def predecir(request):
    if request.method == 'POST':
        estudiante = request.POST.get('estudiante', '').strip()
        anio = request.POST.get('anio')
        periodo = request.POST.get('periodo')

        # Validar que el nombre del estudiante no esté vacío
        if not estudiante:
            messages.error(request, 'Por favor, ingresa el nombre del estudiante.')
            return render(request, 'formulario.html', {
                'materias': materias,
                'valores_anteriores': request.POST
            })

        # Validar que 'anio' y 'periodo' estén presentes y sean números enteros
        try:
            anio = int(anio)
            periodo = int(periodo)
        except (TypeError, ValueError):
            messages.error(request, 'Año y Periodo deben ser números enteros.')
            return render(request, 'formulario.html', {
                'materias': materias,
                'valores_anteriores': request.POST
            })

        # Función para validar y convertir las notas
        def validar_nota(nota):
            if not nota:
                return 0.0
            try:
                nota = float(nota.replace(',', '.'))
                if nota < 0 or nota > 5:
                    raise ValueError("La nota debe estar entre 0 y 5")
                return nota
            except ValueError:
                raise ValueError("Las notas deben ser números entre 0 y 5")

        try:
            # Procesar las notas de las materias
            datos_entrada = {}
            materias_notas = {}
            for materia_nombre, materia_campo in materias.items():
                nota_str = request.POST.get(materia_campo, '0')
                nota = validar_nota(nota_str)
                datos_entrada[materia_nombre] = [nota]
                materias_notas[materia_nombre] = nota

            # Crear DataFrame para el modelo
            X_nuevo = pd.DataFrame(datos_entrada)

            # Realizar la predicción
            y_pred = modelo.predict(X_nuevo)

            carreras = ['Ing. de Sistemas Afines', 'Ing. Industrial', 'Medicina', 'Enfermería', 'Derecho',
                        'Adm Empresas', 'Psicología', 'Contaduría', 'Ing Ambiental', 'Ing Electrónica',
                        'Marketing Digital', 'Ing Mecánica', 'Arquitectura', 'Educación (STEM)',
                        'Economía-finanzas', 'Finanzas RelacionesInte', 'Ing Agronómica',
                        'Biología y Biotecnología', 'Diseño Gráfico Industrial', 'Turismo y Hospitalidad']

            resultados = {carrera: round(prob, 2) for carrera, prob in zip(carreras, y_pred[0])}

            # Serializar resultados a JSON
            resultados_json = json.dumps(resultados)

            # Guardar la predicción en la base de datos
            prediccion = Prediccion(estudiante=estudiante, anio=anio, periodo=periodo, resultados=resultados)
            prediccion.save()

            # Obtener las top 3 carreras recomendadas
            top_3_carreras = sorted(resultados.items(), key=lambda x: x[1], reverse=True)[:3]

            # Obtener las materias con las notas más altas
            materias_top = sorted(materias_notas.items(), key=lambda x: x[1], reverse=True)[:3]

            return render(request, 'resultados.html', {
                'resultados_json': resultados_json,
                'estudiante': estudiante,
                'anio': anio,
                'periodo': periodo,
                'top_3_carreras': top_3_carreras,
                'materias_top': materias_top
            })

        except ValueError as e:
            messages.error(request, f"Error en la entrada: {str(e)}")
            return render(request, 'formulario.html', {
                'materias': materias,
                'valores_anteriores': request.POST
            })

    else:
        # Si es una solicitud GET, mostrar el formulario con valores predeterminados
        valores_anteriores = {
            'estudiante': '',
            'anio': '',
            'periodo': '',
        }
        # Asignar nota predeterminada de 3.0 a todas las materias
        for materia_campo in materias.values():
            valores_anteriores[materia_campo] = 3.0

        return render(request, 'formulario.html', {
            'materias': materias,
            'valores_anteriores': valores_anteriores
        })

def listar_predicciones(request):
    predicciones = Prediccion.objects.all()
    return render(request, 'listar_predicciones.html', {'predicciones': predicciones})

def eliminar_prediccion(request, id):
    try:
        prediccion = Prediccion.objects.get(id=id)
        prediccion.delete()
        messages.success(request, "Predicción eliminada exitosamente.")
    except Prediccion.DoesNotExist:
        messages.error(request, "La predicción no existe o ya ha sido eliminada.")
    return redirect('listar_predicciones')

def modificar_prediccion(request, id):
    prediccion = get_object_or_404(Prediccion, id=id)

    if request.method == 'POST':
        try:
            estudiante = request.POST.get('estudiante', '').strip()
            anio = int(request.POST.get('anio'))
            periodo = int(request.POST.get('periodo'))

            # Validar y obtener las notas de las materias
            def validar_nota(nota):
                if not nota:
                    return 0.0
                nota = float(nota.replace(',', '.'))
                if nota < 0 or nota > 5:
                    raise ValueError("La nota debe estar entre 0 y 5")
                return nota

            materias_notas = {}
            for materia_nombre, materia_campo in materias.items():
                nota_str = request.POST.get(materia_campo, '0')
                nota = validar_nota(nota_str)
                materias_notas[materia_nombre] = nota

            # Crear DataFrame y predecir
            X_nuevo = pd.DataFrame([materias_notas])

            y_pred = modelo.predict(X_nuevo)

            carreras = ['Ing. de Sistemas Afines', 'Ing. Industrial', 'Medicina', 'Enfermería', 'Derecho',
                        'Adm Empresas', 'Psicología', 'Contaduría', 'Ing Ambiental', 'Ing Electrónica',
                        'Marketing Digital', 'Ing Mecánica', 'Arquitectura', 'Educación (STEM)',
                        'Economía-finanzas', 'Finanzas RelacionesInte', 'Ing Agronómica',
                        'Biología y Biotecnología', 'Diseño Gráfico Industrial', 'Turismo y Hospitalidad']

            resultados = {carrera: round(prob, 2) for carrera, prob in zip(carreras, y_pred[0])}

            # Actualizar la predicción existente
            prediccion.estudiante = estudiante
            prediccion.anio = anio
            prediccion.periodo = periodo
            prediccion.resultados = resultados
            prediccion.save()

            # Obtener las top 3 carreras y materias
            top_3_carreras = sorted(resultados.items(), key=lambda x: x[1], reverse=True)[:3]
            materias_top = sorted(materias_notas.items(), key=lambda x: x[1], reverse=True)[:3]

            return render(request, 'resultados.html', {
                'resultados': resultados,
                'estudiante': estudiante,
                'anio': anio,
                'periodo': periodo,
                'top_3_carreras': top_3_carreras,
                'materias_top': materias_top
            })

        except ValueError as e:
            messages.error(request, f"Error en la entrada: {str(e)}")
            return render(request, 'modificar_prediccion.html', {
                'prediccion': prediccion,
                'materias': materias
            })

    else:
        # Aquí cargamos los valores desde la base de datos para mostrarlos en el formulario
        valores_anteriores = {
            'estudiante': prediccion.estudiante,
            'anio': prediccion.anio,
            'periodo': prediccion.periodo,
        }
        for materia_nombre, materia_campo in materias.items():
            # Verificamos si las notas de la base de datos están presentes
            valores_anteriores[materia_campo] = prediccion.resultados.get(materia_nombre, 3.0)

        return render(request, 'modificar_prediccion.html', {
            'prediccion': prediccion,
            'materias': materias,
            'valores_anteriores': valores_anteriores
        })

def comparar_predicciones(request):
    if request.method == 'POST':
        prediccion_ids = request.POST.getlist('prediccion_ids')

        if len(prediccion_ids) < 2:
            messages.error(request, "Debe seleccionar al menos dos predicciones para comparar.")
            return redirect('listar_predicciones')

        predicciones = Prediccion.objects.filter(id__in=prediccion_ids)

        if predicciones.exists():
            sns.set(style="whitegrid", palette="deep")
            fig, ax = plt.subplots(figsize=(12, 8), facecolor='none')

            colors = sns.color_palette("husl", len(predicciones))

            for idx, prediccion in enumerate(predicciones):
                labels = list(prediccion.resultados.keys())
                values = list(prediccion.resultados.values())
                sns.lineplot(x=labels, y=values, marker="o", ax=ax, color=colors[idx], label=f'{prediccion.estudiante} - {prediccion.anio} - {prediccion.periodo}')

            ax.set_xlabel('Carreras', fontsize=14)
            ax.set_ylabel('Puntajes', fontsize=14)

            ax.legend(fontsize=12, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=False)

            ax.set_facecolor('none')
            plt.xticks(rotation=45, ha='right', fontsize=12)
            plt.yticks(fontsize=12)
            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, transparent=True)
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            image_base64 = base64.b64encode(image_png).decode('utf-8')

            return render(request, 'comparar_predicciones.html', {'image_base64': image_base64})
        else:
            messages.error(request, "No se encontraron predicciones.")
            return redirect('listar_predicciones')
    
    return redirect('listar_predicciones')

def visualizar_prediccion(request, id):
    prediccion = get_object_or_404(Prediccion, id=id)
    resultados = prediccion.resultados

    # Serializar resultados a JSON
    resultados_json = json.dumps(resultados)

    # Obtener las top 3 carreras recomendadas
    top_3_carreras = sorted(resultados.items(), key=lambda x: x[1], reverse=True)[:3]

    # Obtener las materias con las notas más altas (asumiendo que tienes acceso a las notas originales)
    # Si las notas no están disponibles, puedes omitir 'materias_top' o manejarlo según tus necesidades
    materias_top = []  # Reemplaza esto si tienes acceso a las notas

    return render(request, 'resultados.html', {
        'resultados_json': resultados_json,
        'estudiante': prediccion.estudiante,
        'anio': prediccion.anio,
        'periodo': prediccion.periodo,
        'top_3_carreras': top_3_carreras,
        'materias_top': materias_top
    })
