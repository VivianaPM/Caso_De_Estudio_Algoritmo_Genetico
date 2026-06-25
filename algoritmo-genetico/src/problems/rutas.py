import random
import numpy as np
from graficar import graficar_ruta

def generar_clientes(n=5):
    """Genera clientes con ubicaciones aleatorias"""
    clientes = {'S': {'ubicacion': (0, 0)}}  # El depósito
    for i in range(1, n + 1):
        clientes[f'C{i}'] = {
            'ubicacion': (random.randint(1, 20), random.randint(1, 20))
        }
    return clientes

def calcular_distancias(clientes):
    """Calcula la matriz de distancias entre todos los clientes"""
    distancias = {}
    for cliente_a in clientes:
        distancias[cliente_a] = {}
        for cliente_b in clientes:
            if cliente_a != cliente_b:
                punto_a = np.array(clientes[cliente_a]['ubicacion'])
                punto_b = np.array(clientes[cliente_b]['ubicacion'])
                distancias[cliente_a][cliente_b] = np.linalg.norm(punto_a - punto_b)
            else:
                distancias[cliente_a][cliente_b] = 0
    return distancias

def generar_ruta_inicial(clientes):
    """Genera una ruta inicial válida usando solo algunos clientes aleatorios"""
    clientes_lista = list(clientes.keys())
    clientes_lista.remove('S')
    num_clientes = random.randint(len(clientes_lista) // 3, (len(clientes_lista) * 2) // 3)
    seleccionados = random.sample(clientes_lista, num_clientes)
    return ['S'] + seleccionados + ['S']

def calcular_fitness(ruta, distancias):
    """Calcula el fitness como el inverso de la distancia total"""
    distancia_total = sum(distancias[ruta[i]][ruta[i + 1]] for i in range(len(ruta) - 1))
    return 1 / distancia_total if distancia_total > 0 else 0

def seleccionar_padres(poblacion, fitness_actual):
    padre1 = random.choices(poblacion, weights=fitness_actual)[0]
    padre2 = random.choices(poblacion, weights=fitness_actual)[0]
    return padre1, padre2

def cruzar(padre1, padre2, tasa_cruce):
    """Realiza el cruce entre dos padres para generar un hijo"""
    if random.random() < tasa_cruce:
        punto_cruce = random.randint(1, len(padre1) - 2)
        hijo = padre1[:punto_cruce]
        for gen in padre2:
            if gen not in hijo and gen != 'S':
                hijo.append(gen)
        hijo.append('S')
    else:
        hijo = padre1[:]
    return hijo

def mutar(hijo, tasa_mutacion):
    """Aplica mutación al hijo con una cierta tasa de mutación"""
    if random.random() < tasa_mutacion and len(hijo) > 3:
        i, j = random.sample(range(1, len(hijo) - 1), 2)
        hijo[i], hijo[j] = hijo[j], hijo[i]

def evolucionar_poblacion(poblacion, fitness_actual, elitismo, tasa_cruce, tasa_mutacion):
    """Evoluciona la población mediante selección, cruce y mutación"""
    nueva_poblacion = []
    
    # Elitismo
    elite = sorted(zip(poblacion, fitness_actual), key=lambda x: x[1], reverse=True)[:elitismo]
    nueva_poblacion.extend([e[0] for e in elite])
    
    # Completar la nueva población
    while len(nueva_poblacion) < len(poblacion):
        padre1, padre2 = seleccionar_padres(poblacion, fitness_actual)
        hijo = cruzar(padre1, padre2, tasa_cruce)
        mutar(hijo, tasa_mutacion)
        nueva_poblacion.append(hijo)
    
    return nueva_poblacion

def algoritmo_genetico(tamaño_poblacion, elitismo, seleccion, tasa_cruce, tasa_mutacion, **kwargs):
    """Implementación del algoritmo genético"""
    num_clientes = kwargs.get('clientes', 10)
    clientes = generar_clientes(num_clientes)
    distancias = calcular_distancias(clientes)
    
    # Generar población inicial
    poblacion = [generar_ruta_inicial(clientes) for _ in range(tamaño_poblacion)]
    
    # # Lista para almacenar el historial de fitness
    historial_fitness = []
    
    # Mejor solución encontrada
    mejor_ruta = None
    mejor_fitness = 0
    
    # Evolución
    for _ in range(100):  # 100 generaciones
        # Calcular fitness de la población actual
        fitness_actual = [calcular_fitness(ruta, distancias) for ruta in poblacion]
        
        # Actualizar mejor solución
        mejor_idx = fitness_actual.index(max(fitness_actual))
        if fitness_actual[mejor_idx] > mejor_fitness:
            mejor_fitness = fitness_actual[mejor_idx]
            mejor_ruta = poblacion[mejor_idx]
        
        # Guardar el mejor fitness de esta generación
        historial_fitness.append(mejor_fitness)
        
        # Crear nueva población
        poblacion = evolucionar_poblacion(poblacion, fitness_actual, elitismo, tasa_cruce, tasa_mutacion)
    graficar_ruta(mejor_ruta, clientes, distancias)
    return mejor_ruta, mejor_fitness, historial_fitness, poblacion

def mostrar_resultados(mejor_ruta, mejor_fitness, num_clientes, poblacion_inicial, poblacion_final):
    """Muestra los resultados del algoritmo genético"""
    print("\nResultados:")
    print(f"Mejor ruta encontrada: {' -> '.join(mejor_ruta)}")
    print(f"Fitness de la solución: {mejor_fitness:.4f}")
    print(f"Número de clientes visitados: {len(mejor_ruta) - 2}")  # -2 por los depósitos
    print(f"Número de clientes no visitados: {num_clientes - (len(mejor_ruta) - 2)}")
    
    print("\nPoblación inicial:")
    print(poblacion_inicial)
    print("Población final:")
    print(len(poblacion_final))
