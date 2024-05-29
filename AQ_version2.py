import random
import math
import csv

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


def seleccionar_mejor_individuo(poblacion, matriz):
    mejor_individuo = poblacion[0]
    mejor_energia = calcular_energia(mejor_individuo[next(iter(mejor_individuo))], matriz)
    for individuo in poblacion:
        energia = calcular_energia(individuo[next(iter(individuo))], matriz)
        if energia < mejor_energia:
            mejor_individuo, mejor_energia = individuo, energia
    return mejor_individuo, mejor_energia


def seleccionar_una_poblacion(poblacion, n):
    return random.sample(poblacion, n)


def combinar(individuo1, individuo2):
    # Obtener el índice de los individuos en S
    index1 = next(iter(individuo1))
    index2 = next(iter(individuo2))
    punto_cruce = random.randrange(2, 11)
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

    # Asegurarse de que los nuevos individuos tengan todos los elementos necesarios
    todos_elementos = set(range(1, len(individuo1[index1]) - 1))

    # Encontrar los elementos que faltan
    faltantes1 = list(todos_elementos - set(nuevo_individuo1))
    faltantes2 = list(todos_elementos - set(nuevo_individuo2))

    # Añadir los elementos que faltan para completar
    nuevo_individuo1.extend(faltantes1)
    nuevo_individuo2.extend(faltantes2)

    if nuevo_individuo1[-1] != 0:
        nuevo_individuo1.append(0)

    if nuevo_individuo2[-1] != 0:
        nuevo_individuo2.append(0)

    return nuevo_individuo1, nuevo_individuo2


def perturbar_con_reaccion_quimica(S, buffer, poblacion, KEL, matriz):
    ran = random.randint(1, 4)
    if ran == 1:
        S, buffer = contra_pared(S, buffer, KEL)
    elif ran == 2:
        S, buffer = descomposicion(S, buffer, KEL, poblacion, matriz)
    elif ran == 3:
        ran2 = random.randrange(0, len(poblacion) - 1)
        S2 = poblacion[ran2]
        intramolecular_ineficaz(S, S2, buffer, KEL, poblacion, matriz)
    elif ran == 4:
        ran2 = random.randrange(0, len(poblacion) - 1)
        S2 = poblacion[ran2]
        sintesis(S, S2, buffer, KEL, poblacion, matriz)
    return S, buffer


def contra_pared(S, buffer, KEL):
    index = next(iter(S))
    Snew = S[index][1:-1]
    random.shuffle(Snew)
    Snew = [0] + Snew + [0]
    EPnew = calcular_energia(Snew, cost_matriz)
    new = {index: Snew, 'EP': EPnew, 'EK': 0}

    if S['EP'] + S['EK'] >= new['EP']:
        q = random.uniform(KEL, 1)
        KEnew = (S['EP'] + S['EK'] - new['EP']) * q
        buffer += (S['EP'] + S['EK'] - new['EP']) * (1 - q)
        S[index] = new[index][:]
        S['EP'] = new['EP']
        S['EK'] = KEnew
    return S, buffer


def intramolecular_ineficaz(S1, S2, buffer, KEL, poblacion, matriz):
    index1 = next(iter(S1))
    index2 = next(iter(S2))

    Snew1 = S1[index1][1:-1]
    random.shuffle(Snew1)
    Snew1 = [0] + Snew1 + [0]

    Snew2 = S2[index2][1:-1]
    random.shuffle(Snew2)
    Snew2 = [0] + Snew2 + [0]

    EPnew1 = calcular_energia(Snew1, matriz)
    EPnew2 = calcular_energia(Snew2, matriz)

    new1 = {'i1': Snew1, 'EP': EPnew1, 'EK': 0}
    new2 = {'i2': Snew2, 'EP': EPnew2, 'EK': 0}

    if S1['EP'] + S1['EK'] >= new1['EP']:
        q = random.uniform(KEL, 1)
        KEnew = (S1['EP'] + S1['EK'] - new1['EP']) * q
        buffer += (S1['EP'] + S1['EK'] - new1['EP']) * (1 - q)
        S1[index1] = new1['i1'][:]
        S1['EP'] = new1['EP']
        S1['EK'] = KEnew

    if S2['EP'] + S2['EK'] >= new2['EP']:
        q = random.uniform(KEL, 1)
        KEnew = (S2['EP'] + S2['EK'] - new2['EP']) * q
        buffer += (S2['EP'] + S2['EK'] - new2['EP']) * (1 - q)
        S2[index2] = new2['i2'][:]
        S2['EP'] = new2['EP']
        S2['EK'] = KEnew

    return S1, S2, buffer


def descomposicion(S, buffer, KEL, poblacion, matriz):
    index = next(iter(S))
    KE2 = S['EK'] / 2
    S['EK'] = KE2
    KE3 = S['EK'] / 2
    S['EK'] = KE3

    Snew = S[index][1:-1]
    random.shuffle(Snew)
    Snew = [0] + Snew + [0]

    EPnew = calcular_energia(Snew, matriz)
    new = {index: Snew, 'EP': EPnew, 'EK': KE2}

    poblacion.append(new)
    return S, buffer


def sintesis(S1, S2, buffer, KEL, poblacion, matriz):
    Snew1, Snew2 = combinar(S1, S2)

    EPnew1 = calcular_energia(Snew1, matriz)
    EPnew2 = calcular_energia(Snew2, matriz)

    new1 = {'i1': Snew1, 'EP': EPnew1, 'EK': 0}
    new2 = {'i2': Snew2, 'EP': EPnew2, 'EK': 0}

    poblacion.append(new1)
    poblacion.append(new2)
    return S1, S2, buffer


def enfriamiento_simulado(S, matriz):
    T = 1000
    r = 0.95
    max_epocas = 1000
    for epoca in range(max_epocas):
        for i in range(100):
            nuevo_S = S[:]
            # Perturbar la solución actual
            i, j = random.sample(range(1, len(nuevo_S) - 1), 2)
            nuevo_S[i], nuevo_S[j] = nuevo_S[j], nuevo_S[i]
            EPnuevo = calcular_energia(nuevo_S, matriz)
            Eactual = calcular_energia(S, matriz)
            delta_E = EPnuevo - Eactual
            if delta_E < 0 or random.random() < math.exp(-delta_E / T):
                S = nuevo_S
        T *= r
    return S


# Parcheo de función principal
def main():
    poblacion = crear_poblacion_inicial(100, cost_matriz)
    mejor_solucion, mejor_energia = seleccionar_mejor_individuo(poblacion, cost_matriz)

    buffer = 0
    KEL = 0.8

    for iteracion in range(100):
        seleccion = seleccionar_una_poblacion(poblacion, 5)
        for S in seleccion:
            S, buffer = perturbar_con_reaccion_quimica(S, buffer, poblacion, KEL, cost_matriz)

        nueva_mejor_solucion, nueva_mejor_energia = seleccionar_mejor_individuo(poblacion, cost_matriz)
        if nueva_mejor_energia < mejor_energia:
            mejor_solucion, mejor_energia = nueva_mejor_solucion, nueva_mejor_energia

    print("Mejor solución encontrada:", mejor_solucion)
    print("Mejor energía:", mejor_energia)


if __name__ == "__main__":
    main()
