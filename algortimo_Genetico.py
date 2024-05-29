
import random

# Definir la matriz de costos
cost_matriz = [[-1,513,507,1190,1100,1150,1280,1230,1120,1270,1030,1000,962],
         [518,-1,100,804,714,804,928,1210,1100,1220,1030,1010,968],
         [495,82,-1,755,661,748,869,1120,1020,1140,947,926,883],
         [1190,795,747,-1,99,82,155,925,880,899,873,863,851],
         [1090,704,656,101,-1,96,214,886,831,867,814,805,787],
         [1160,799,741,79,97,-1,123,845,802,817,799,786,775],
         [1270,915,863,148,216,118,-1,840,812,806,817,809,804],
         [1220,1200,1120,926,886,841,835,-1,115,57,200,221,273],
         [1100,1090,1010,878,829,798,813,118,-1,164,84,110,152],
         [1260,1220,1140,895,863,820,803,63,159,-1,252,269,314],
         [1010,1030,944,869,811,789,815,200,90,246,-1,23,68],
         [987,1010,922,864,804,785,816,229,116,269,26,-1,43],
         [938,958,877,850,787,773,809,273,165,315,162,50,-1]
         ]


def calcular_energia(solucion, matriz):
    distancia = 0
    for i in range(len(solucion) - 1):
        distancia += matriz[solucion[i]][solucion[i + 1]]
    return distancia

def energia_total(poblacion):
    Etotal = 0
    for celula in poblacion:
        Etotal += celula["EP"]
    return Etotal

def crear_solucion_aleatoria(matriz):
    lugares = list(range(1, len(matriz)))  # Excluye el punto de inicio (0)
    random.shuffle(lugares)
    return [0] + lugares + [0]  # Empieza y termina en 0

def crear_poblacion_inicial(n, matriz):
    poblacion = []
    for i in range(n):
        individuo = crear_solucion_aleatoria(matriz)
        energia_potencial = calcular_energia(individuo, matriz)
        poblacion.append({
            i: individuo,
            "EP": energia_potencial,
            "EK": 0  
        })
    return poblacion  



# Función para seleccionar los padres (torneo)
def selection(population):
    fitness_scores = [individuo["EP"] for individuo in population]
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:
        return random.sample(population, 2)
    probabilities = [score / total_fitness for score in fitness_scores]
    selected = random.choices(population, weights=probabilities, k=2)
    return selected[0], selected[1]

#Funcion para combinar los individuos
def combinar(individuo1, individuo2):
    index1 = next(iter(individuo1))
    index2 = next(iter(individuo2))
    punto_cruce = random.randrange(2, len(individuo1[index1]) - 2)
    a = individuo1[index1][:punto_cruce]
    b = individuo1[index1][punto_cruce:]
    c = individuo2[index2][:punto_cruce]
    d = individuo2[index2][punto_cruce:]

    nuevo_individuo1 = a[:]
    nuevo_individuo2 = c[:]

    for nodo in d:
        if nodo not in nuevo_individuo1:
            nuevo_individuo1.append(nodo)
    
    for nodo in b:
        if nodo not in nuevo_individuo2:
            nuevo_individuo2.append(nodo)

    todos_elementos = set(range(1, len(individuo1[index1]) - 1))
    faltantes1 = list(todos_elementos - set(nuevo_individuo1))
    faltantes2 = list(todos_elementos - set(nuevo_individuo2))

    nuevo_individuo1.extend(faltantes1)
    nuevo_individuo2.extend(faltantes2)
    
    nuevo_individuo1.append(0)
    nuevo_individuo2.append(0)

    return {index1: nuevo_individuo1, "EP": calcular_energia(nuevo_individuo1, cost_matriz)}, {index2: nuevo_individuo2, "EP": calcular_energia(nuevo_individuo2, cost_matriz)}



def mutacion(individual, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(1, len(individual) - 1), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual


def algoritmo_genetico(matriz, num_generaciones=500, tamano_poblacion=100, tasa_mutacion=0.01):
    poblacion = crear_poblacion_inicial(tamano_poblacion, matriz)

    for generacion in range(num_generaciones):
        nueva_poblacion = []

        for _ in range(tamano_poblacion // 2):
            padre1, padre2 = selection(poblacion)
            hijo1, hijo2 = combinar(padre1, padre2)

            mutacion(hijo1[next(iter(hijo1))], tasa_mutacion)
            mutacion(hijo2[next(iter(hijo2))], tasa_mutacion)

            nueva_poblacion.append(hijo1)
            nueva_poblacion.append(hijo2)

        poblacion = nueva_poblacion

    mejor_individuo = min(poblacion, key=lambda ind: ind["EP"])
    mejor_ruta = mejor_individuo[next(iter(mejor_individuo))]
    mejor_costo = mejor_individuo["EP"]

    return mejor_ruta, mejor_costo

# Ejecutar el algoritmo genético
mejor_ruta, mejor_costo = algoritmo_genetico(cost_matriz)

print("La mejor solución encontrada es:")
print(mejor_ruta)
print("Con un costo total de:")
print(mejor_costo)
