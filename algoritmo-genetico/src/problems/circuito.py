# circuito.py
import random
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tqdm import tqdm

from graficar import graficar_circuito

# Definición de los componentes como rectángulos con dimensiones
componentes = [
    (4, 3),  # Rectángulo 1 (ancho=4, alto=3)
    (3, 2),  # Rectángulo 2
    (5, 2),  # Rectángulo 3
    (5, 5),  # Rectángulo 4
    (5, 1)   # Rectángulo 5
]

# Definición de las relaciones entre los componentes
relaciones_componentes = {
    0: [1, 4],  # Componente 0 está relacionado con el componente 1 y 4
    1: [0, 2],  # Componente 1 está relacionado con el componente 0 y el componente 2
    2: [1, 3],
    4: [1],
    3: [2]
}

# Definición del área de trabajo (por ejemplo, 100x100)
ancho_area_trabajo = 100
alto_area_trabajo = 100

def generar_cromosoma(componentes, ancho_area_trabajo, alto_area_trabajo):
    cromosoma = []
    for ancho, alto in componentes:
        x = random.randint(0, ancho_area_trabajo - ancho)
        y = random.randint(0, alto_area_trabajo - alto)
        cromosoma.append((x, y))
    return cromosoma

def generar_poblacion(tamano_poblacion, componentes, ancho_area_trabajo, alto_area_trabajo):
    return [generar_cromosoma(componentes, ancho_area_trabajo, alto_area_trabajo) for _ in range(tamano_poblacion)]

def is_overlapping(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

def calcular_fitness(cromosoma):
    penalizacion = 0
    area_ocupada = 0
    n = len(cromosoma)

    max_x, min_x, max_y, min_y = float('-inf'), float('inf'), float('-inf'), float('inf')
    for i in range(n):
        x, y = cromosoma[i]
        ancho, alto = componentes[i]
        max_x = max(max_x, x + ancho)
        min_x = min(min_x, x)
        max_y = max(max_y, y + alto)
        min_y = min(min_y, y)
        area_ocupada += ancho * alto

        for j in range(i + 1, n):
            if is_overlapping((x, y, ancho, alto), (cromosoma[j][0], cromosoma[j][1], componentes[j][0], componentes[j][1])):
                penalizacion += 1000  # Gran penalización por solapamiento

    area_total = (max_x - min_x) * (max_y - min_y)
    fitness = area_total - area_ocupada + penalizacion
    return fitness

def evolucionar(tamano_poblacion=1000, num_generaciones=100):
    poblacion = generar_poblacion(tamano_poblacion, componentes, ancho_area_trabajo, alto_area_trabajo)
    historial_fitness = []

    for generacion in tqdm(range(num_generaciones), desc="Generaciones"):
        fitness_poblacion = [calcular_fitness(cromosoma) for cromosoma in poblacion]
        mejor_fitness_generacion = min(fitness_poblacion)
        historial_fitness.append(mejor_fitness_generacion)

        # Selección, cruce y mutación (simplificado)
        nueva_poblacion = sorted(zip(poblacion, fitness_poblacion), key=lambda x: x[1])[:2]  # Elitismo
        while len(nueva_poblacion) < tamano_poblacion:
            padres = random.sample(poblacion, 2)
            descendiente = generar_cromosoma(componentes, ancho_area_trabajo, alto_area_trabajo)
            nueva_poblacion.append((descendiente, calcular_fitness(descendiente)))  # Añadir el descendiente y su fitness

        poblacion = [cromosoma for cromosoma, _ in nueva_poblacion]

    mejor_cromosoma = poblacion[fitness_poblacion.index(min(fitness_poblacion))]
    return mejor_cromosoma, min(fitness_poblacion), historial_fitness

def ejecutar_diseño_circuitos():
    mejor_cromosoma, mejor_fitness, historial_fitness = evolucionar()
    print("\nResultados del diseño de circuitos:")
    print(f"Población inicial: 1000")
    print(f"Población final: {len(historial_fitness)}")
    print(f"Valor de la función de aptitud del mejor individuo: {mejor_fitness:.4f}")

    # Mostrar las coordenadas del mejor cromosoma
    print("Mejor disposición de componentes (coordenadas):")
    for idx, (x, y) in enumerate(mejor_cromosoma):
        print(f"Componente {idx + 1}: (x={x}, y={y})")
    
    graficar_circuito(mejor_cromosoma, componentes, ancho_area_trabajo, alto_area_trabajo, relaciones_componentes)

    return historial_fitness
# def evolucionar(config):
#     """Evoluciona la población de cromosomas según la configuración dada."""
#     tamano_poblacion = config['tamaño_poblacion']
#     num_generaciones = config['num_generaciones']
#     componentes = config['num_componentes']  # Asegúrate de que esto sea correcto
#     ancho_area_trabajo = config['ancho_area_trabajo']
#     alto_area_trabajo = config['alto_area_trabajo']

#     poblacion = generar_poblacion(tamano_poblacion, componentes, ancho_area_trabajo, alto_area_trabajo)
#     historial_fitness = []

#     for generacion in tqdm(range(num_generaciones), desc="Generaciones"):
#         fitness_poblacion = [calcular_fitness(cromosoma) for cromosoma in poblacion]
#         mejor_fitness_generacion = min(fitness_poblacion)
#         historial_fitness.append(mejor_fitness_generacion)

#         # Selección, cruce y mutación (simplificado)
#         nueva_poblacion = sorted(zip(poblacion, fitness_poblacion), key=lambda x: x[1])[:2]  # Elitismo
#         while len(nueva_poblacion) < tamano_poblacion:
#             padres = random.sample(poblacion, 2)
#             descendiente = generar_cromosoma(componentes, ancho_area_trabajo, alto_area_trabajo)
#             nueva_poblacion.append((descendiente, calcular_fitness(descendiente)))  # Añadir el descendiente y su fitness

#         poblacion = [cromosoma for cromosoma, _ in nueva_poblacion]

#     mejor_cromosoma = poblacion[fitness_poblacion.index(min(fitness_poblacion))]
#     return mejor_cromosoma, min(fitness_poblacion), historial_fitness

# def ejecutar_diseño_circuitos(tamaño_poblacion, elitismo, seleccion, tasa_cruce, tasa_mutacion, num_componentes, ancho_area_trabajo, alto_area_trabajo):
#     # Definir el número de generaciones
#     num_generaciones = 100  # Ajusta este valor según sea necesario

#     # Generar una lista de componentes aleatorios o predeterminados
#     componentes = [(random.randint(1, 10), random.randint(1, 10)) for _ in range(num_componentes)]  # Ejemplo de componentes

#     config = {
#         'tamaño_poblacion': tamaño_poblacion,
#         'elitismo': elitismo,
#         'seleccion': seleccion,
#         'tasa_cruce': tasa_cruce,
#         'tasa_mutacion': tasa_mutacion,
#         'num_componentes': num_componentes,
#         'ancho_area_trabajo': ancho_area_trabajo,
#         'alto_area_trabajo': alto_area_trabajo,
#         'num_generaciones': num_generaciones,  # Asegúrate de incluir el número de generaciones
#         'componentes': componentes  # Asegúrate de incluir la lista de componentes
#     }
    
#     mejor_cromosoma, mejor_fitness, historial_fitness = evolucionar(config)
    
#     print("\nResultados del diseño de circuitos:")
#     print(f"Población inicial: {tamaño_poblacion}")
#     print(f"Población final: {len(historial_fitness)}")
#     print(f"Valor de la función de aptitud del mejor individuo: {mejor_fitness:.4f}")

#     # Mostrar las coordenadas del mejor cromosoma
#     print("Mejor disposición de componentes (coordenadas):")
#     for idx, (x, y) in enumerate(mejor_cromosoma):
#         print(f"Componente {idx + 1}: (x={x}, y={y})")
    
#     graficar_circuito(mejor_cromosoma, componentes, ancho_area_trabajo, alto_area_trabajo)

#     return historial_fitness