import random

# Define the cost matrix
cost_matriz = [[-1, 513, 507, 1190, 1100, 1150, 1280, 1230, 1120, 1270, 1030, 1000, 962],
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
               [938, 958, 877, 850, 787, 773, 809, 273, 165, 315, 162, 50, -1]]

# Function to calculate the energy (cost) of a solution
def calcular_energia(solucion, matriz):
    distancia = 0
    for i in range(len(solucion) - 1):
        distancia += matriz[solucion[i]][solucion[i + 1]]
    return distancia

# Function to create a random solution
def crear_solucion_aleatoria(matriz):
    lugares = list(range(1, len(matriz)))  # Exclude the starting point (0)
    random.shuffle(lugares)
    return [0] + lugares + [0]  # Start and end at 0

# Function to create the initial population
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

# Function to select the best individual from the population
def selecciona_el_mejor_individuo(poblacion, matriz):
    mejor_individuo = poblacion[0]
    mejor_energia = calcular_energia(mejor_individuo[next(iter(mejor_individuo))], matriz)
    for individuo in poblacion:
        energia = calcular_energia(individuo[next(iter(individuo))], matriz)
        if energia < mejor_energia:
            mejor_individuo, mejor_energia = individuo, energia
    return mejor_individuo, mejor_energia

# Mutation function to introduce variations
def mutacion(individuo):
    index = next(iter(individuo))
    Snew = individuo[index][1:-1].copy()
    a, b = random.sample(range(1, len(Snew) - 1), 2)
    Snew[a], Snew[b] = Snew[b], Snew[a]
    Snew = [0] + Snew + [0]
    individuo[index] = Snew
    return individuo

# Function to combine two individuals to create offspring
def combinar(individuo1, individuo2):
    index1 = next(iter(individuo1))
    index2 = next(iter(individuo2))
    punto_cruce = random.randrange(2, 11)
    a = individuo1[index1][:punto_cruce]
    b = individuo1[index1][punto_cruce:]
    c = individuo2[index2][:punto_cruce]
    d = individuo2[index2][punto_cruce:]

    nuevo_individuo1 = a + [nodo for nodo in d if nodo not in a]
    nuevo_individuo2 = c + [nodo for nodo in b if nodo not in c]

    todos_elementos = set(range(1, len(individuo1[index1]) - 1))
    faltantes1 = list(todos_elementos - set(nuevo_individuo1))
    faltantes2 = list(todos_elementos - set(nuevo_individuo2))

    nuevo_individuo1.extend(faltantes1)
    nuevo_individuo2.extend(faltantes2)

    if nuevo_individuo1[-1] != 0:
        nuevo_individuo1.append(0)
    if nuevo_individuo2[-1] != 0:
        nuevo_individuo2.append(0)

    individuo1[index1] = nuevo_individuo1
    individuo2[index2] = nuevo_individuo2
    return individuo1, individuo2

# Perturbation function using chemical reactions concepts
def perturbar_con_reaccion_quimica(S, buffer, poblacion, KEL, matriz):
    ran = random.randint(1, 4)
    if ran == 1:
        S, buffer = contra_pared(S, buffer, KEL, poblacion)
    elif ran == 2:
        S, S2, buffer = descomposicion(S, buffer, poblacion, matriz)
    elif ran == 3:
        ran2 = random.randrange(0, len(poblacion))
        S2 = poblacion[ran2]
        S, buffer = intramolecular_ineficaz(S, S2, buffer, poblacion, matriz)
    elif ran == 4:
        ran2 = random.randrange(0, len(poblacion))
        S2 = poblacion[ran2]
        S, buffer = sintesis(S, S2, buffer, poblacion, matriz)
    return S, buffer

def contra_pared(S, buffer, KEL, poblacion):
    index = next(iter(S))
    length = len(poblacion)
    Snew = S[index][1:-1].copy()
    a, b = random.sample(range(1, len(Snew) - 1), 2)
    Snew[a], Snew[b] = Snew[b], Snew[a]
    Snew = [0] + Snew + [0]
    
    EPnew = calcular_energia(Snew, cost_matriz)
    new = {length: Snew, 'EP': EPnew, 'EK': 0}

    if S['EP'] + S['EK'] >= new['EP']:
        q = random.uniform(KEL, 1)
        KEnew = (S['EP'] + S['EK'] - new['EP']) * q
        buffer += (S['EP'] + S['EK'] - new['EP']) * (1 - q)
        S[index] = new[length].copy()
        S['EP'] = new['EP']
        S['EK'] = KEnew
    return S, buffer

def intramolecular_ineficaz(S1, S2, buffer, poblacion, matriz):
    index1 = next(iter(S1))
    index2 = next(iter(S2))

    length = len(poblacion)
    Snew1 = S1[index1][1:-1].copy()
    random.shuffle(Snew1)
    Snew1 = [0] + Snew1 + [0]

    Snew2 = S2[index2][1:-1].copy()
    random.shuffle(Snew2)
    Snew2 = [0] + Snew2 + [0]

    EPnew1 = calcular_energia(Snew1, matriz)
    EPnew2 = calcular_energia(Snew2, matriz)

    new1 = {length: Snew1, 'EP': EPnew1, 'EK': 0}
    new2 = {length + 1: Snew2, 'EP': EPnew2, 'EK': 0}

    temp = (S1['EP'] + S1['EK']) + (S2['EP'] + S2['EK']) - new1['EP'] - new2['EP']
    if temp >= 0:
        q = random.uniform(0, 1)
        KEnew1 = temp * q
        KEnew2 = temp * (1 - q)
        buffer += (S1['EP'] + S1['EK']) + (S2['EP'] + S2['EK']) - temp
        S1[index1] = new1[length].copy()
        S1['EP'] = new1['EP']
        S1['EK'] = KEnew1

        S2[index2] = new2[length + 1].copy()
        S2['EP'] = new2['EP']
        S2['EK'] = KEnew2

    return S1, buffer

def descomposicion(S1, buffer, poblacion, matriz):
    index1 = next(iter(S1))

    length = len(poblacion)
    Snew1 = S1[index1][1:-1].copy()
    random.shuffle(Snew1)
    Snew1 = [0] + Snew1 + [0]

    EPnew1 = calcular_energia(Snew1, matriz)

    new1 = {length: Snew1, 'EP': EPnew1, 'EK': 0}

    S2 = mutacion(S1.copy())
    EPnew2 = calcular_energia(S2[index1], matriz)

    temp = (S1['EP'] + S1['EK']) - (new1['EP'] + EPnew2)
    if temp >= 0:
        q = random.uniform(0, 1)
        KEnew1 = temp * q
        KEnew2 = temp * (1 - q)
        buffer += (S1['EP'] + S1['EK']) - temp
        S1[index1] = new1[length].copy()
        S1['EP'] = new1['EP']
        S1['EK'] = KEnew1
        S2[index1] = S2[index1].copy()
        S2['EP'] = EPnew2
        S2['EK'] = KEnew2
    return S1, S2, buffer

def sintesis(S1, S2, buffer, poblacion, matriz):
    S1, S2 = combinar(S1, S2)
    index1 = next(iter(S1))
    index2 = next(iter(S2))

    length = len(poblacion)
    Snew1 = S1[index1]
    Snew2 = S2[index2]

    EPnew1 = calcular_energia(Snew1, matriz)
    EPnew2 = calcular_energia(Snew2, matriz)

    new1 = {length: Snew1, 'EP': EPnew1, 'EK': 0}
    new2 = {length + 1: Snew2, 'EP': EPnew2, 'EK': 0}

    temp = (S1['EP'] + S1['EK']) + (S2['EP'] + S2['EK']) - new1['EP']
    if temp >= 0:
        KEnew1 = temp
        buffer += (S1['EP'] + S1['EK']) + (S2['EP'] + S2['EK']) - temp
        S1[index1] = new1[length].copy()
        S1['EP'] = new1['EP']
        S1['EK'] = KEnew1

    return S1, buffer

def main():
    generaciones = 1000
    num_individuos = 100
    poblacion = crear_poblacion_inicial(num_individuos, cost_matriz)

    KE = 10000
    KEL = 0.2
    buffer = 0
    for i in range(generaciones):
        S, E = selecciona_el_mejor_individuo(poblacion, cost_matriz)
        S, buffer = perturbar_con_reaccion_quimica(S, buffer, poblacion, KEL, cost_matriz)
        E2 = S['EP']
        poblacion.append(S)
        poblacion = sorted(poblacion, key=lambda x: x['EP'])[:num_individuos]
        
        if i % 100 == 0:
            print(f"Generación {i}, mejor solución: {E2}")

    mejor, energia = selecciona_el_mejor_individuo(poblacion, cost_matriz)
    print(f"Mejor solución final: {mejor}, energía: {energia}")

if __name__ == "__main__":
    main()
