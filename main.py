from algoritmo_genetico.src.UI.menu import mostrar_menu, obtener_datos_problema
from algoritmo_genetico.src.problems.rutas import algoritmo_genetico, mostrar_resultados
from algoritmo_genetico.src.problems.circuito import ejecutar_diseño_circuitos
from algoritmo_genetico.src.problems.cartera import ejecutar_inversiones_cartera
from algoritmo_genetico.src.utils.graficar import graficar_fitness

def main():
    while True:
        mostrar_menu()
        opcion = input("Ingrese el número de la opción: ")

        if opcion == '4':
            print("Saliendo del programa...")
            break
        elif opcion in ['1', '2', '3']:
            try:
                datos = obtener_datos_problema(int(opcion))
                if not datos:
                    print("No se encontraron datos para este problema.")
                    continue

                print("\nResolviendo problema...")
                if opcion == '1':  # Rutas de Entrega
                    mejor_ruta, mejor_fitness, historial_fitness, poblacion_final = algoritmo_genetico(**datos)
                    
                    # Construir el diccionario de resultados
                    resultados = {
                        'mejor_ruta': mejor_ruta,
                        'mejor_fitness': mejor_fitness,
                        'num_clientes': datos['clientes'], 
                        'poblacion_inicial': datos['tamaño_poblacion'], 
                        'poblacion_final': poblacion_final
                    }
                    # Mostrar resultados
                    mostrar_resultados(**resultados)
                    graficar_fitness(historial_fitness)
                elif opcion == '2':  # Diseño de Circuitos
                    historial_fitness = ejecutar_diseño_circuitos()
                    graficar_fitness(historial_fitness)
                elif opcion == '3':  # Cartera de Inversiones
                    historial_fitness = ejecutar_inversiones_cartera(**datos)
                    graficar_fitness(historial_fitness)
            except Exception as e:
                print(f"Se ha producido un error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()