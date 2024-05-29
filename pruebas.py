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

def combinar(individuo1, individuo2):
    # Obtener el índice de los individuos en S
    index1 = next(iter(individuo1))
    index2 = next(iter(individuo2))
    punto_cruce=random.randrange(2,11)
    a=individuo1[index1][:punto_cruce]
    b=individuo1[index1][punto_cruce:]
    c=individuo2[index2][:punto_cruce]
    d=individuo2[index2][punto_cruce:]

    nuevo_individuo1=a[:]
    nuevo_individuo2=c[:]
    
    for nodo in d:
        if not nodo in nuevo_individuo1:
            nuevo_individuo1.append(nodo)

    
    for nodo in b:
        if nodo not in nuevo_individuo2:
            nuevo_individuo2.append(nodo)

    # Asegurarse de que los nuevos individuos tengan todos los elementos necesarios
    # Obtener todos los elementos posibles
    todos_elementos = set(range(len(individuo1)-1))
    
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

def contra_pared(S1,S2, buffer,KEL,poblacion,matriz):    
    # Obtener el índice de los individuos en S
    index1 = next(iter(S1))
    index2 = next(iter(S2))
    length=len(poblacion)
    
    Snew1,Snew2=combinar(S1,S2)
    
    #Obtener energia de los individuos
    EPnew1=calcular_energia(Snew1,matriz)
    EPnew2=calcular_energia(Snew2,matriz)
    
    new1={length:Snew1, 'EP': EPnew1, 'EK':0}
    new2={length:Snew2, 'EP': EPnew2, 'EK':0}
    
    if new1['EP']>new2['EP']:
        nuevo_individuo=new1
    else:
        nuevo_individuo=new2
    
    temp=(S1['EP']+S2['EP']+S1['EK']+S2['EK'])-(new1['EP']+new2['EP'])
    success=False
    if S1['EP']+S2['EP']+S1['EK']+S2['EK']>=nuevo_individuo['EP']:
        success=True
        EKnuevo= S1['EP']+S2['EP']+S1['EK']+S2['EK'] - nuevo_individuo['EP']
        nuevo_individuo['EK']=EKnuevo
        poblacion.append(nuevo_individuo)
    else:
        success=False
    return nuevo_individuo, success,buffer

def energia_total(poblacion):
    Etotal = 0
    for celula in poblacion:
        Etotal += celula["EP"]
    return Etotal

def ejecutar(matriz):
    individuos=50
    poblacion=crear_poblacion_inicial(individuos,matriz)
    ran1=random.randrange(0,individuos-1)  
    ran2=random.randrange(0,individuos-1)  
    
    Etotal=energia_total(poblacion)
    KEL=0.1
    buffer=Etotal*0.10
    S1=poblacion[ran1]
    S2=poblacion[ran2]
    
    print(S1,S2)
    S,success,buffer=contra_pared(S1,S2,buffer,KEL,poblacion,matriz)
    print(S)
    
    
    
    
        
ejecutar(matriz=cost_matriz)