import random
import math
import csv

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
    # Calcula la energía total de la solución basada en la matriz de costos.
    distancia = 0
    for i in range(len(solucion) - 1):
        distancia+= matriz[solucion[i]][solucion[i + 1]]
    return distancia

def crear_solucion_aleatoria(matriz):
    lugares = list(range(1, len(matriz)))  # Excluye el punto de inicio (0)
    random.shuffle(lugares)
    return [0] + lugares + [0]   # Empieza y termina en 0

def crear_poblacion_inicial(n, matriz):
    return [crear_solucion_aleatoria(matriz) for _ in range(n)]

def combinar(individuo1, individuo2):
    punto_cruce=random.randrange(2,11)
    a=individuo1[:punto_cruce]
    b=individuo1[punto_cruce:]
    c=individuo2[:punto_cruce]
    d=individuo2[punto_cruce:]

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

def selecciona_el_mejor_individuo(poblacion, matriz):
    mejor_individuo = poblacion[0]
    mejor_energia = calcular_energia(mejor_individuo, matriz)
    for individuo in poblacion:
        energia = calcular_energia(individuo, matriz)
        if energia < mejor_energia:
            mejor_individuo, mejor_energia = individuo, energia
    return mejor_individuo, mejor_energia

def seleccionar_una_poblacion(poblacion, n):
    return random.sample(poblacion, n)

def simulated_annealing(matriz, temp_inicial, temp_final, coef_enfriamiento):
    #Realiza la búsqueda de la mejor solución utilizando el algoritmo de enfriamiento simulado.
    T = temp_inicial
    Tf = temp_final
    individuos=50
    poblacion=crear_poblacion_inicial(individuos,matriz)
    S,ES=selecciona_el_mejor_individuo(poblacion,matriz)
    Smejor = S
    ESmejor = ES
    while T > Tf:
        n=1
        while n<=300: 
            Solucion = seleccionar_una_poblacion(poblacion, 1)[0]
            Snew1,Snew2 = combinar(S, Solucion)
            poblacion.append(Snew1)
            poblacion.append(Snew2)
            
            temp=[Snew1,Snew2]
            Snew,ESnew=  selecciona_el_mejor_individuo(temp,matriz)         
            diferencia = ESnew - ES

            # Si la nueva solución es mejor, o se acepta una peor con cierta probabilidad para evitar mínimos locales
            if diferencia < 0:
                S = Snew
                ES = ESnew
                # Si la nueva solución es la mejor hasta el momento, se actualiza Smejor y ESmejor
                if ES < ESmejor:
                    Smejor = S[:]
                    ESmejor = ES
                    
            else:
                probabilidad=math.exp(-diferencia / T) 
                if probabilidad> random.random():
                    S=Snew
                    ES=ESnew 
                    
            n+=1

        # Se enfría la temperatura según la tasa de enfriamiento
        T *= coef_enfriamiento 
          
    return Smejor, ESmejor

# Parámetros para el algoritmo
temp_inicial = 10000
temp_final = 0.01
coef_enfriamiento = 0.99

# Ejecución del algoritmo de enfriamiento simulado con la matriz de costos de ejemplo

def muestra():
    mu=[]
    avg=0
    for i in range(0,30):
        temp=[]
        best_solucion, best_energy = simulated_annealing(cost_matriz, temp_inicial, temp_final, coef_enfriamiento)
        temp=[best_solucion, best_energy]
        mu.append(temp)
        avg+=best_energy
        print (best_solucion, best_energy)
        
        
    avg=avg/30
    

# best_solucion, best_energy = simulated_annealing(cost_matriz, temp_inicial, temp_final, coef_enfriamiento)
# print (best_solucion, best_energy)
muestra()
