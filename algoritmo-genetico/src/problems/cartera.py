import random
import numpy as np
from deap import base, creator, tools
from graficar import graficar_cartera

def optimizar_cartera(config):
    # Datos de ejemplo para los activos
    NUM_ASSETS = config['num_activos']
    EXPECTED_RETURNS = np.random.uniform(0.05, 0.15, NUM_ASSETS)  # Rendimientos aleatorios
    VOLATILITIES = np.random.uniform(0.05, 0.2, NUM_ASSETS)  # Volatilidades aleatorias
    BUDGET = 1.0
    MAX_INVESTMENT = 0.2

    # Crear tipos de individuos
    creator.create("FitnessMax", base.Fitness, weights=(1.0, -1.0))  # Maximizar rendimiento, minimizar riesgo
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    # Atributos y generación de individuos
    def generate_individual():
        proportions = np.random.dirichlet(np.ones(NUM_ASSETS), size=1)[0]
        proportions = np.clip(proportions, 0, MAX_INVESTMENT)
        proportions /= sum(proportions)
        return proportions.tolist()

    toolbox.register("individual", tools.initIterate, creator.Individual, generate_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Función de evaluación
    def evaluate(individual):
        expected_return = np.dot(individual, EXPECTED_RETURNS)
        risk = np.sqrt(np.dot(individual, np.dot(np.diag(VOLATILITIES), individual)))
        return expected_return, risk

    # Operadores genéticos
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.01, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("evaluate", evaluate)

    # Algoritmo genético
    random.seed(42)
    pop = toolbox.population(n=config['tamaño_poblacion'])
    hof = tools.HallOfFame(config['elitismo'])
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    logbook = []
    ngen = 500

    for gen in range(ngen):
        # Selección y clonación
        offspring = toolbox.select(pop, len(pop) - len(hof))
        offspring = list(map(toolbox.clone, offspring))

        # Cruce
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < config['tasa_cruce']:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Mutación
        for mutant in offspring:
            if random.random() < config['tasa_mutacion']:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluar individuos con fitness inválido
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Reemplazar la población antigua con la nueva
        pop[:] = tools.selBest(pop, len(hof)) + offspring

        # Actualizar el Hall of Fame con la población actual
        hof.update(pop)

        # Estadísticas
        record = stats.compile(pop)
        logbook.append(record)
        # print(f"Generación {gen + 1}: {record}")

        # Parada por fitness menor a 10^-2
        if any(ind.fitness.values[1] < 10**-2 for ind in pop):
            print(f"Parada por fitness menor a 10^-2 en la generación {gen + 1}")
            break

    return pop, logbook, hof

def ejecutar_inversiones_cartera(tamaño_poblacion, elitismo, seleccion, tasa_cruce, tasa_mutacion, num_activos):
    config = {
        'tamaño_poblacion': tamaño_poblacion,
        'elitismo': elitismo,
        'seleccion': seleccion,
        'tasa_cruce': tasa_cruce,
        'tasa_mutacion': tasa_mutacion,
        'num_activos': num_activos
    }
    pop, logbook, hof = optimizar_cartera(config)
    mejor_fitness = hof[0].fitness.values[0]
    historial_fitness = [record['max'] for record in logbook] 
    # print("Historial de fitness:", historial_fitness)  # Verifica el contenido

    print("\nResultados del diseño de circuitos:")
    print(f"Población inicial: {tamaño_poblacion}")
    print(f"Población final: {len(historial_fitness)}")
    print(f"Valor de la función de aptitud del mejor individuo: {mejor_fitness:.4f}")

    # Mostrar las coordenadas del mejor cromosoma
    print("Mejor disposición de componentes (coordenadas):", hof[0])

    graficar_cartera(pop, logbook, hof)

    return historial_fitness