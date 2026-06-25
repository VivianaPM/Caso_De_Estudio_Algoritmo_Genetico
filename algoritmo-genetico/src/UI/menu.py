def mostrar_menu():
    print("\nSeleccione un problema a resolver con el algoritmo genético:")
    print("1. Optimización de Rutas de Entrega")
    print("2. Optimización del Diseño de Circuitos Electrónicos")
    print("3. Optimización de la Cartera de Inversiones")
    print("4. Salir")

def obtener_datos_problema(opcion):
    if opcion == 1:  # Optimización de rutas de entrega
        return {
            'tamaño_poblacion': 1000,
            'elitismo': 2,
            'seleccion': 'torneo',
            'tasa_cruce': 0.9,
            'tasa_mutacion': 0.02,
            'numero_camiones': 1,
            'clientes': 15,
            'capacidad_maxima': 30
        }
    elif opcion == 2:
        return {
            'tamaño_poblacion': 1000,
            'elitismo': 2,
            'seleccion': 'torneo',
            'tasa_cruce': 0.90,
            'tasa_mutacion': 0.02,
            'num_componentes': 50,
            'ancho_area_trabajo': 100,  # Define el ancho del área de trabajo
            'alto_area_trabajo': 100     # Define el alto del área de trabajo
        }
    elif opcion == 3:
        return {
            'tamaño_poblacion': 1000,
            'elitismo': 2,
            'seleccion': 'torneo',
            'tasa_cruce': 0.90,
            'tasa_mutacion': 0.02,
            'num_activos': 20
        }
    else:
        return None