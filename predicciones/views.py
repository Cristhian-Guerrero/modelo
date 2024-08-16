import seaborn as sns
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import matplotlib.pyplot as plt
import io
import urllib, base64
import joblib
import pandas as pd
from .models import Prediccion

# Cargar el modelo entrenado
modelo = joblib.load('predicciones/modelo_entrenado.pkl')

def inicio(request):
    return render(request, 'inicio.html')

def predecir(request):
    if request.method == 'POST':
        try:
            def validar_nota(nota):
                nota = float(nota.replace(',', '.'))
                if nota < 0 or nota > 5:
                    raise ValueError("La nota debe estar entre 0 y 5")
                return nota

            estudiante = request.POST.get('estudiante', 'Anónimo')
            anio = int(request.POST.get('anio'))
            periodo = int(request.POST.get('periodo'))

            datos_entrada = {
                'Matemáticas': [validar_nota(request.POST.get('matematicas', 0))],
                'Español': [validar_nota(request.POST.get('espanol', 0))],
                'Biología': [validar_nota(request.POST.get('biologia', 0))],
                'C-Sociales': [validar_nota(request.POST.get('c_sociales', 0))],
                'Inglés': [validar_nota(request.POST.get('ingles', 0))],
                'Edu-Física': [validar_nota(request.POST.get('edu_fisica', 0))],
                'Informática': [validar_nota(request.POST.get('informatica', 0))],
                'Artes': [validar_nota(request.POST.get('artes', 0))],
                'Religión': [validar_nota(request.POST.get('religion', 0))],
                'Filosofía': [validar_nota(request.POST.get('filosofia', 0))],
                'Economía': [validar_nota(request.POST.get('economia', 0))]
            }

            X_nuevo = pd.DataFrame(datos_entrada)
            y_pred = modelo.predict(X_nuevo)

            carreras = ['Ing. de Sistemas Afines', 'Ing. Industrial', 'Medicina', 'Enfermería', 'Derecho', 
                        'Adm Empresas', 'Psicología', 'Contaduría', 'Ing Ambiental', 'Ing Electrónica', 
                        'Marketing Digital', 'Ing Mecánica', 'Arquitectura', 'Educación (STEM)', 
                        'Economía-finanzas', 'Finanzas RelacionesInte', 'Ing Agronómica', 
                        'Biología y Biotecnología', 'Diseño Gráfico Industrial', 'Turismo y Hospitalidad']

            resultados = {carrera: round(p, 2) for carrera, p in zip(carreras, y_pred[0])}

            # Obtener las 3 carreras más probables
            top_3_carreras = sorted(resultados.items(), key=lambda x: x[1], reverse=True)[:3]

            # Obtener las materias con las notas más altas
            top_materias = sorted({k: v[0] for k, v in datos_entrada.items()}.items(), key=lambda x: x[1], reverse=True)[:3]

            # Guardar la predicción
            prediccion = Prediccion(estudiante=estudiante, anio=anio, periodo=periodo, resultados=resultados)
            prediccion.save()

            return render(request, 'resultados.html', {
                'resultados': resultados,
                'estudiante': estudiante,
                'anio': anio,
                'periodo': periodo,
                'top_3_carreras': top_3_carreras,
                'top_materias': top_materias,
            })

        except ValueError as e:
            messages.error(request, f"Error en la entrada: {str(e)}")
            return render(request, 'formulario.html')

    return render(request, 'formulario.html')


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
            def validar_nota(nota):
                nota = float(nota.replace(',', '.'))
                if nota < 0 or nota > 5:
                    raise ValueError("La nota debe estar entre 0 y 5")
                return nota

            estudiante = request.POST.get('estudiante', 'Anónimo')
            anio = int(request.POST.get('anio'))
            periodo = int(request.POST.get('periodo'))

            datos_entrada = {
                'Matemáticas': [validar_nota(request.POST['matematicas'])],
                'Español': [validar_nota(request.POST['espanol'])],
                'Biología': [validar_nota(request.POST['biologia'])],
                'C-Sociales': [validar_nota(request.POST['c_sociales'])],
                'Inglés': [validar_nota(request.POST['ingles'])],
                'Edu-Física': [validar_nota(request.POST['edu_fisica'])],
                'Informática': [validar_nota(request.POST['informatica'])],
                'Artes': [validar_nota(request.POST['artes'])],
                'Religión': [validar_nota(request.POST['religion'])],
                'Filosofía': [validar_nota(request.POST['filosofia'])],
                'Economía': [validar_nota(request.POST['economia'])]
            }

            # Convertir datos de entrada a un DataFrame
            X_nuevo = pd.DataFrame(datos_entrada)
            y_pred = modelo.predict(X_nuevo)

            carreras = ['Ing. de Sistemas Afines', 'Ing. Industrial', 'Medicina', 'Enfermería', 'Derecho', 
                        'Adm Empresas', 'Psicología', 'Contaduría', 'Ing Ambiental', 'Ing Electrónica', 
                        'Marketing Digital', 'Ing Mecánica', 'Arquitectura', 'Educación (STEM)', 
                        'Economía-finanzas', 'Finanzas RelacionesInte', 'Ing Agronómica', 
                        'Biología y Biotecnología', 'Diseño Gráfico Industrial', 'Turismo y Hospitalidad']

            resultados = {carrera: round(p, 2) for carrera, p in zip(carreras, y_pred[0])}

            # Actualizar la predicción existente
            prediccion.estudiante = estudiante
            prediccion.anio = anio
            prediccion.periodo = periodo
            prediccion.resultados = resultados
            prediccion.save()

            return redirect('listar_predicciones')

        except ValueError as e:
            from django.contrib import messages
            messages.error(request, f"Error en la entrada: {str(e)}")
            return render(request, 'modificar_prediccion.html', {'prediccion': prediccion})

    return render(request, 'modificar_prediccion.html', {'prediccion': prediccion})

def comparar_predicciones(request):
    if request.method == 'POST':
        prediccion_ids = request.POST.getlist('prediccion_ids')

        if len(prediccion_ids) < 2:
            messages.error(request, "Debe seleccionar al menos dos predicciones para comparar.")
            return redirect('listar_predicciones')

        predicciones = Prediccion.objects.filter(id__in=prediccion_ids)

        if predicciones.exists():
            sns.set(style="whitegrid", palette="deep")  # Tema moderno con colores más oscuros
            fig, ax = plt.subplots(figsize=(12, 8), facecolor='none')  # Tamaño ajustado de la gráfica, sin fondo

            # Colores consistentes
            colors = sns.color_palette("husl", len(predicciones))

            for idx, prediccion in enumerate(predicciones):
                labels = list(prediccion.resultados.keys())
                values = list(prediccion.resultados.values())
                sns.lineplot(x=labels, y=values, marker="o", ax=ax, color=colors[idx], label=f'{prediccion.estudiante} - {prediccion.anio} - {prediccion.periodo}')

            ax.set_xlabel('Carreras', fontsize=14, color='#333')
            ax.set_ylabel('Puntajes', fontsize=14, color='#333')
            ax.set_title('', fontsize=16, color='#333')

            # Mover la leyenda fuera de la gráfica, centrada arriba
            ax.legend(fontsize=12, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=False)

            # Ajustar el fondo de los ejes para que sea transparente
            ax.set_facecolor('none')

            # Mejorar la legibilidad de las etiquetas
            plt.xticks(rotation=45, ha='right', fontsize=12)
            plt.yticks(fontsize=12)

            # Ajustar los márgenes para evitar que los elementos se vean apretados
            plt.subplots_adjust(top=0.85, bottom=0.15, left=0.1, right=0.9)

            # Ajustar el diseño para evitar que los elementos se superpongan
            plt.tight_layout()

            # Convertir la gráfica a una imagen en base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, transparent=True)  # Alta resolución con fondo transparente
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            image_base64 = base64.b64encode(image_png).decode('utf-8')

            context = {
                'image_base64': image_base64,
            }

            return render(request, 'comparar_predicciones.html', context)
        else:
            messages.error(request, "No se encontraron predicciones.")
            return redirect('listar_predicciones')
    
    return redirect('listar_predicciones')

def visualizar_prediccion(request, id):
    prediccion = get_object_or_404(Prediccion, id=id)
    resultados = prediccion.resultados
    
    return render(request, 'resultados.html', {
        'resultados': resultados,
        'estudiante': prediccion.estudiante,
        'anio': prediccion.anio,
        'periodo': prediccion.periodo
    })
