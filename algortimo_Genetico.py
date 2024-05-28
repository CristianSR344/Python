import numpy as np
import random

# Definir la matriz de costos
cost_matrix = np.array([
    [-1, 513, 507, 1190, 1100, 1150, 1280, 1230, 1120, 1270, 1030, 1000, 962],
    [518, -1, 100, 804, 714, 804, 928, 1210, 1100, 1220, 1030, 1010, 968],
    [495, 82, -1, 755, 661, 748, 869, 1120, 1020, 1140, 947, 926, 883],
    [1190, 795, 747, -1, 99, 82, 155, 925, 880, 899, 873, 863, 851],
    [1090, 704, 656, 101, -1, 96, 214, 886, 831, 867, 814, 805, 787],
    [1160, 799, 741, 79, 97, -1, 123, 845, 802, 817, 799, 786, 775],
    [1270, 915, 863, 148, 216, 118, -1, 840, 812, 806, 817, 809, 804],
    [1220, 1200, 1120, 926, 886, 841, 835, -1, 115, 57, 200, 221, 273],
    [1100, 1090, 1010, 878, 829, 798, 813, 118, -1, 164, 84, 110, 152],
    [1260, 1220, 1140, 895, 863, 820, 803, 63, 159, -1, 252, 269, 314],
    [1010, 1030, 944, 869, 811, 789, 815, 200, 90, 246, -1, 23, 68],
    [987, 1010, 922, 864, 804, 785, 816, 229, 116, 269, 26, -1, 43],
    [938, 958, 877, 850, 787, 773, 809, 273, 165, 315, 162, 50, -1]
])

# Configuraciones del algoritmo genético
POPULATION_SIZE = 100
GENERATIONS = 1000
MUTATION_RATE = 0.01
ELITE_SIZE = 5

# Función para crear un individuo (una ruta aleatoria)
def create_individual(num_nodes):
    return random.sample(range(num_nodes), num_nodes)

# Función para calcular la aptitud (el costo total de la ruta)
def calculate_fitness(individual, cost_matrix):
    cost = 0
    for i in range(len(individual) - 1):
        cost += cost_matrix[individual[i], individual[i + 1]]
    cost += cost_matrix[individual[-1], individual[0]]  # Regresar al punto de partida
    return cost

# Función para seleccionar los padres (torneo)
def selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:
        return random.sample(population, 2)
    probabilities = [score / total_fitness for score in fitness_scores]
    selected = random.choices(population, weights=probabilities, k=2)
    return selected[0], selected[1]

# Función para hacer el cruce (crossover) de dos padres
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]

    pointer = 0
    for i in range(size):
        if child[i] is None:
            while parent2[pointer] in child:
                pointer += 1
            child[i] = parent2[pointer]
    return child

# Función para mutar un individuo
def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

# Inicializar la población
num_nodes = len(cost_matrix)
population = [create_individual(num_nodes) for _ in range(POPULATION_SIZE)]

# Algoritmo genético
for generation in range(GENERATIONS):
    # Calcular la aptitud de la población
    fitness_scores = [1 / calculate_fitness(ind, cost_matrix) for ind in population]
    
    # Asegurarse de que las aptitudes sean positivas
    min_fitness = min(fitness_scores)
    if min_fitness <= 0:
        fitness_scores = [score - min_fitness + 1 for score in fitness_scores]

    # Selección de la próxima generación
    next_population = []
    for _ in range(ELITE_SIZE):
        next_population.append(population[np.argmax(fitness_scores)])
        fitness_scores[np.argmax(fitness_scores)] = -1  # Excluir a los mejores para mantener la diversidad

    while len(next_population) < POPULATION_SIZE:
        parent1, parent2 = selection(population, fitness_scores)
        child = crossover(parent1, parent2)
        child = mutate(child, MUTATION_RATE)
        next_population.append(child)

    population = next_population

# Encontrar la mejor solución
best_individual = min(population, key=lambda ind: calculate_fitness(ind, cost_matrix))
best_cost = calculate_fitness(best_individual, cost_matrix)

print("La mejor solución encontrada es:")
print(best_individual)
print("Con un costo total de:")
print(best_cost)
