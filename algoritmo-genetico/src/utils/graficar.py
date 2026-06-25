from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np

def graficar_fitness(historial_fitness):
    # Verificar que historial_fitness no esté vacío y no contenga None
    if not historial_fitness or any(fit is None for fit in historial_fitness):
        print("Error: historial_fitness contiene valores None o está vacío.")
        return

    plt.plot(historial_fitness)
    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.title("Evolución de la Aptitud (Mayor es Mejor)")
    plt.grid()
    plt.show()

def calcular_fitness(cromosoma, distancias):
    """
    Calcula el fitness de una ruta basado en las distancias entre los clientes.
    El fitness se calcula como el inverso de la distancia total recorrida.
    """
    distancia_total = 0
    for i in range(len(cromosoma) - 1):
        distancia_total += distancias[cromosoma[i]][cromosoma[i + 1]]
    return 1 / distancia_total if distancia_total > 0 else float('inf')

def graficar_ruta(ruta, clientes, distancias):
    if not ruta or not clientes:
        print("No hay datos suficientes para graficar la ruta")
        return

    # Convertir las ubicaciones a una lista de coordenadas
    ubicaciones = []
    ubicaciones.append((0, 0))  # Punto inicial (depósito)
    
    for cliente in ruta:
        if cliente in clientes and 'ubicacion' in clientes[cliente]:
            ubicaciones.append(clientes[cliente]['ubicacion'])
    
    if len(ubicaciones) < 2:
        print("No hay suficientes puntos para graficar una ruta")
        return

    ubicaciones = np.array(ubicaciones)
    
    plt.figure(figsize=(10, 8))
    
    # Graficar la ruta
    plt.plot(ubicaciones[:, 0], ubicaciones[:, 1], 'bo-', label="Ruta")
    
    # Marcar el depósito
    plt.scatter(0, 0, color='red', s=100, marker='s', label="Depósito")
    
    # Marcar los clientes
    for i, (x, y) in enumerate(ubicaciones[1:], 1):
        plt.scatter(x, y, color='blue')
        plt.annotate(f'C{i}', (x, y), xytext=(5, 5), textcoords='offset points')
    
    plt.title("Ruta de Entrega")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.show()

def graficar_circuito(cromosoma, componentes, ancho_area_trabajo, alto_area_trabajo, relaciones_componentes=None):
    fig, ax = plt.subplots()

    # Calcular los límites del área de trabajo
    max_x = ancho_area_trabajo
    max_y = alto_area_trabajo

    # Ajustar la vista de la gráfica para mostrar todos los componentes
    ax.set_xlim(0, max_x)
    ax.set_ylim(0, max_y)
    ax.set_aspect('equal')

    # Dibujar los componentes
    for idx, ((x, y), (ancho, alto)) in enumerate(zip(cromosoma, componentes)):
        rect = patches.Rectangle((x, y), ancho, alto, linewidth=1, edgecolor='r', facecolor='none', zorder=2)
        ax.add_patch(rect)
        ax.annotate(f'C{idx + 1}', (x + ancho / 2, y + alto / 2), color='blue', weight='bold',
                    fontsize=12, ha='center', va='center')

    # Mostrar las relaciones entre componentes como líneas tenues
    if relaciones_componentes:
        for componente, relacionados in relaciones_componentes.items():
            x1, y1 = cromosoma[componente][0] + componentes[componente][0] / 2, cromosoma[componente][1] + componentes[componente][1] / 2
            for relacionado in relacionados:
                x2, y2 = cromosoma[relacionado][0] + componentes[relacionado][0] / 2, cromosoma[relacionado][1] + componentes[relacionado][1] / 2
                ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.3)  # Línea tenue

    plt.gca().invert_yaxis()  # Invertir el eje Y para que el origen esté en la parte superior izquierda
    plt.title("Disposición de Componentes en el Circuito")
    plt.xlabel("Ancho del Área de Trabajo")
    plt.ylabel("Alto del Área de Trabajo")
    plt.grid(True)
    plt.show()

import matplotlib.pyplot as plt

def graficar_cartera(pop, logbook, hof):
    gen = range(1, len(logbook) + 1)
    fit_mins = [record['min'] for record in logbook]
    fit_maxs = [record['max'] for record in logbook]
    fit_avgs = [record['avg'] for record in logbook]

    # Graficar los resultados de evolución de fitness
    plt.figure(figsize=(12, 6))
    plt.plot(gen, fit_avgs, label="Aptitud Promedio")
    plt.plot(gen, fit_maxs, label="Aptitud Máxima")
    plt.plot(gen, fit_mins, label="Aptitud Mínima")
    plt.xlabel("Generación")
    plt.ylabel("Aptitud")
    plt.title("Evolución de la Aptitud")
    plt.legend(loc="best")
    plt.grid()
    plt.show()