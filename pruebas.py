import random
import copy
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

def calcular_energia(solucion, matriz):
    distancia = 0
    for i in range(len(solucion) - 1):
        distancia += matriz[solucion[i]][solucion[i + 1]]
    return distancia

def contra_pared(S, buffer,KEL,poblacion,matriz):
    print("Estado inicial de S:", S)
    length = len(poblacion)
    
    # Obtener el índice del individuo en S
    index = next(iter(S))
    
    # Obtener la estructura actual y mantener el primer y último elemento como 0
    estructura_actual = S[index]
    
    # Definir un punto de cruce aleatorio
    punto_cruce = random.randrange(2, len(estructura_actual) - 2)
    
    # Dividir la estructura en dos partes
    a = estructura_actual[:punto_cruce]
    b = estructura_actual[punto_cruce:]
    print("Parte A:", a)
    print("Parte B:", b)
    
    # Crear dos nuevos individuos a partir de las dos partes
    nuevo_individuo1 = a[:]
    nuevo_individuo2 = b[:-1]
    
    # Obtener todos los elementos posibles
    todos_elementos = set(range(1, len(estructura_actual) - 1))
    
    # Encontrar los elementos que faltan
    faltantes1 = list(todos_elementos - set(nuevo_individuo1))
    faltantes2 = list(todos_elementos - set(nuevo_individuo2))

    # Añadir los elementos que faltan para completar
    nuevo_individuo1.extend(faltantes1)
    nuevo_individuo2.extend(faltantes2)

    # Asegurar que ambos individuos comiencen y terminen en 0
    if nuevo_individuo1[-1] != 0:
        nuevo_individuo1.append(0)
    if nuevo_individuo2[-1] != 0:
        nuevo_individuo2.append(0)
    if nuevo_individuo1[0] != 0:
        nuevo_individuo1.insert(0, 0)
    if nuevo_individuo2[0] != 0:
        nuevo_individuo2.insert(0, 0)

    # Calcular la energía potencial de las nuevas estructuras
    EPnew1 = calcular_energia(nuevo_individuo1, cost_matriz)
    EPnew2 = calcular_energia(nuevo_individuo2, cost_matriz)
    
    # Crear los nuevos individuos
    new1 = {length: nuevo_individuo1, 'EP': EPnew1, 'EK': 0}
    new2 = {length+1: nuevo_individuo2, 'EP': EPnew2, 'EK': 0}
    
    print("Nuevo individuo 1:", new1)
    print("Nuevo individuo 2:", new2)

    # Seleccionar el mejor nuevo individuo (con menor energía potencial)
    if new1['EP'] < new2['EP']:
        new = new1
    else:
        new = new2

    

    temp=S['EP']+S['EK']-new1['EP']-new2['EP']
    success=False

    if temp>=0:
        success=True
        k=random.randrange(0,1)
        new1['EK']=temp*k
        new2['EK']=temp*(1-k)
        # Agregar los nuevos individuos a la población
        poblacion.append(new1)
        poblacion.append(new2)
    elif temp+buffer>=0:
        success=True
        m1=random.randrange(0,1)
        m2=random.randrange(0,1)
        m3=random.randrange(0,1)
        m4=random.randrange(0,1)
        new1['EK']=(temp+buffer) *m1*m2
        new2['EK']=(temp+buffer-new1['EK'])*m3*m4
        buffer=temp+buffer-new1['EK']-new2['EK']
        # Agregar los nuevos individuos a la población
        poblacion.append(new1)
        poblacion.append(new2)
    else:
        success=False

    for individuo in poblacion:
        print(individuo)
    return S, buffer

def energia_total(poblacion):
    Etotal = 0
    for celula in poblacion:
        Etotal += celula["EP"]
    return Etotal

def ejecutar(matriz):
    individuos=50
    poblacion=crear_poblacion_inicial(individuos,matriz)
    ran=random.randrange(0,individuos-1)  
    Etotal=energia_total(poblacion)
    KEL=0.1
    buffer=Etotal*0.10
    S=poblacion[ran]

    S,buffer=contra_pared(S,buffer,KEL,poblacion,matriz)

    
    
    
    
        
ejecutar(matriz=cost_matriz)