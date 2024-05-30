import random
import math

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





def mutacion(individuo):
    index = next(iter(individuo))
    Snew = individuo[index][1:-1].copy()
    a, b = random.sample(range(1, len(Snew) - 1), 2)  # Elige dos puntos para intercambiar, sin incluir el primero y el último (0)
    Snew[a], Snew[b] = Snew[b], Snew[a]
    Snew = [0] + Snew + [0]

    return individuo 

def calcular_energia(solucion, matriz):

    distancia = 0
    for i in range(len(solucion) - 1):
        distancia += matriz[solucion[i]][solucion[i + 1]]
    return distancia

def calcular_energia_ind(solucion, matriz):
    index1 = next(iter(solucion))
    solucion=solucion[index1][:]
    distancia = 0
    for i in range(len(solucion) - 1):
        distancia += matriz[solucion[i]][solucion[i + 1]]
        
    return distancia

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

n=0
def selecciona_el_mejor_individuo(poblacion, matriz):
    mejor_individuo = poblacion[0]
    mejor_energia = calcular_energia(mejor_individuo[next(iter(mejor_individuo))], matriz)
    for individuo in range(len(poblacion)-1):
        energia = calcular_energia_ind(poblacion[individuo], matriz)
        if energia < mejor_energia:
            mejor_individuo, mejor_energia = individuo, energia
    mejor_individuo =poblacion[mejor_individuo]
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

    nuevo_individuo1 = a[:].copy()
    nuevo_individuo2 = c[:].copy()

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

    nuevo_individuo1.extend(faltantes1)
    nuevo_individuo2.extend(faltantes2)

    if nuevo_individuo1[-1] != 0:
        nuevo_individuo1.append(0)

    if nuevo_individuo2[-1] != 0:
        nuevo_individuo2.append(0)

    individuo1[index1]=nuevo_individuo1.copy()
    individuo2[index2]=nuevo_individuo2.copy()
    return individuo1, individuo2


def perturbar_con_reaccion_quimica(S, buffer, poblacion, KEL, matriz):
    ran = random.randint(1, 4)
    if ran == 1:
        S, buffer = contra_pared(S, buffer, KEL,poblacion)
    elif ran == 2:
        S,S2, buffer = descomposicion(S, buffer, poblacion, matriz)
    elif ran == 3:
        ran2 = random.randrange(0, len(poblacion))
        S2 = poblacion[ran2]
        S, buffer = intramolecular_ineficaz(S, S2, buffer, poblacion, matriz)
    elif ran == 4:
        ran2 = random.randrange(0, len(poblacion))
        S2 = poblacion[ran2]
        S, buffer = sintesis(S, S2, buffer, poblacion, matriz)
    return S, buffer


def contra_pared(S, buffer, KEL,poblacion):
    index = next(iter(S))
    length=len(poblacion)
    Snew = S[index][1:-1].copy()
    a, b = random.sample(range(1, len(Snew) - 1), 2)  # Elige dos puntos para intercambiar, sin incluir el primero y el último (0)
    Snew[a], Snew[b] = Snew[b], Snew[a]
    Snew = [0] + Snew + [0]
    

    EPnew = calcular_energia(Snew, cost_matriz)
    new = {length: Snew, 'EP': EPnew, 'EK': 0}

    if S['EP'] + S['EK'] >= new['EP']:
        q = random.uniform(KEL, 1)
        KEnew = (S['EP'] + S['EK'] - new['EP']) * q
        buffer += (S['EP'] + S['EK'] - new['EP']) * (1 - q)
        S[index] = new[length][:].copy()
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
    new2 = {length+1: Snew2, 'EP': EPnew2, 'EK': 0}

    temp = (S1['EP'] + S2['EP'] + S1['EK'] + S2['EK']) - (new1['EP'] + new2['EP'])

    if temp >= 0:
        p = random.random()
        EKnew1 = temp * p
        EKnew2 = temp * (1 - p)
        S1[index1] = new1[length][:].copy()
        S1['EP'] = new1['EP']
        S1['EK'] = EKnew1
        S2[index2] = new2[length+1][:].copy()
        S2['EP'] = new2['EP']
        S2['EK'] = EKnew2

    if S1['EP'] > S2['EP']:
        return S1, buffer
    else:
        return S2, buffer


def descomposicion(S, buffer, poblacion, matriz):
    index = next(iter(S))

    estructura_actual = S[index].copy()

    punto_cruce = random.randrange(1, len(estructura_actual) - 1)

    a = estructura_actual[1:punto_cruce]
    b = estructura_actual[punto_cruce:-1]

    nuevo_individuo1 = a.copy()
    nuevo_individuo2 = b.copy()
    

    
    todos_elementos = set(range(1, len(estructura_actual) - 1))

    faltantes1 = list(todos_elementos - set(nuevo_individuo1))
    faltantes2 = list(todos_elementos - set(nuevo_individuo2))

    nuevo_individuo1.extend(faltantes1)
    nuevo_individuo2.extend(faltantes2)

    if nuevo_individuo1[-1] != 0:
        nuevo_individuo1.append(0)
    if nuevo_individuo2[-1] != 0:
        nuevo_individuo2.append(0)
    if nuevo_individuo1[0] != 0:
        nuevo_individuo1.insert(0, 0)
    if nuevo_individuo2[0] != 0:
        nuevo_individuo2.insert(0, 0)

    EPnew1 = calcular_energia(nuevo_individuo1, matriz)
    EPnew2 = calcular_energia(nuevo_individuo2, matriz)

    length = len(poblacion)
    new1 = {length: nuevo_individuo1, 'EP': EPnew1, 'EK': 0}
    new2 = {length + 1: nuevo_individuo2, 'EP': EPnew2, 'EK': 0}

    temp = S['EP'] + S['EK'] - new1['EP'] - new2['EP']
    if temp >= 0:
        k = random.random()
        new1['EK'] = temp * k
        new2['EK'] = temp * (1 - k)
        poblacion.append(new1)
        poblacion.append(new2)
    elif temp + buffer >= 0:
        m1 = random.random()
        m2 = random.random()
        m3 = random.random()
        m4 = random.random()
        new1['EK'] = (temp + buffer) * m1 * m2
        new2['EK'] = (temp + buffer - new1['EK']) * m3 * m4
        buffer = temp + buffer - new1['EK'] - new2['EK']
        poblacion.append(new1)
        poblacion.append(new2)
    else:
        pass

    return new1,new2, buffer


def sintesis(S1, S2, buffer, poblacion, matriz):

    Snew1, Snew2 = combinar(S1, S2)

    EPnew1 = calcular_energia_ind(Snew1, matriz)
    EPnew2 = calcular_energia_ind(Snew2, matriz)

    length = len(poblacion)
    new1 = {length: Snew1, 'EP': EPnew1, 'EK': 0}
    new2 = {length + 1: Snew2, 'EP': EPnew2, 'EK': 0}

    temp = S1['EP'] + S1['EK'] + S2['EP'] + S2['EK'] - new1['EP'] - new2['EP']
    if temp >= 0:
        k = random.random()
        new1['EK'] = temp * k
        new2['EK'] = temp * (1 - k)
        poblacion.append(new1)
        poblacion.append(new2)
    elif temp + buffer >= 0:
        m1 = random.random()
        m2 = random.random()
        m3 = random.random()
        m4 = random.random()
        new1['EK'] = (temp + buffer) * m1 * m2
        new2['EK'] = (temp + buffer - new1['EK']) * m3 * m4
        buffer = temp + buffer - new1['EK'] - new2['EK']
        poblacion.append(new1)
        poblacion.append(new2)
    else:
        pass

    return S1, buffer


def energia_total(poblacion):
    Etotal = 0
    for celula in poblacion:
        Etotal += celula["EP"]
    return Etotal




def algoritmo_genetico(matriz, num_generaciones, tamano_poblacion, tasa_mutacion):
    poblacion = crear_poblacion_inicial(tamano_poblacion, matriz)
    n=0
    num_individuos = 100
    Etotal=energia_total(poblacion)
    buffer=Etotal/0.5
    while n<num_generaciones:
        KEL=random.randrange(0,1)
        mejor,Emejor=selecciona_el_mejor_individuo(poblacion, matriz)
        individuo=random.choice(poblacion)
        #Se combinan los individuos
        Snew1,Snew2=combinar(mejor,individuo)
        Snew1,buffer= perturbar_con_reaccion_quimica(Snew1, buffer,poblacion,KEL,matriz)
        Snew2,buffer= perturbar_con_reaccion_quimica(Snew2, buffer,poblacion,KEL,matriz)

        index1 = next(iter(Snew1))
        index2 = next(iter(Snew2))

        #Calcular la energia de los individuos
        ESnew1=Snew1['EP']
        ESnew2=Snew2['EP']
        
        poblacion.append(Snew1)
        poblacion.append(Snew2)  
        bandera=False
        #Compara para encontrar el mejor individuo
        if(ESnew1>ESnew2):
            mejor_actual=Snew1
        else:
            mejor_actual=Snew2
        
        if  random.random()<tasa_mutacion:
             mutar=mutacion(mejor_actual)
        
        poblacion.append(mejor_actual)
        
        #Ingresa los individuos a la poblacion
        Emejor_actual=mejor_actual['EP']
        
        #Acepta al mejor actual como el mejor
        if Emejor_actual<Emejor:
            mejor, Emejor=mejor_actual,Emejor_actual
         
        S, E = selecciona_el_mejor_individuo(poblacion, cost_matriz)
        S, buffer = perturbar_con_reaccion_quimica(S, buffer, poblacion, KEL, cost_matriz)
        E2 = S['EP']
        poblacion.append(S)
        poblacion = sorted(poblacion, key=lambda x: x['EP'])[:num_individuos]
        
  
        n+=1
     
    
    return mejor, Emejor

tasa_mutacion = 0.1
tamano_poblacion = 100
num_generaciones = 300
# Ejecutar el algoritmo genético
mejor_ruta, mejor_costo = algoritmo_genetico(cost_matriz, num_generaciones, tamano_poblacion, tasa_mutacion)

def nombres(lista,lugares):
    nueva_lista = []
    for i in lista:
        nueva_lista.append(lugares[i][1])
    return nueva_lista

def muestra():
    mu=[]
    avg=0
    for i in range(0,30):
        temp=[]
        mejor_ruta, mejor_costo = algoritmo_genetico(cost_matriz, num_generaciones, tamano_poblacion, tasa_mutacion)
        print(mejor_ruta,mejor_costo)
        temp=[mejor_ruta, mejor_costo]
        mu.append(temp)
        avg+=mejor_costo
        
    avg=avg/30
    print(avg)


mejor_ruta, mejor_costo = algoritmo_genetico(cost_matriz, num_generaciones, tamano_poblacion, tasa_mutacion)

print(mejor_ruta,mejor_costo)