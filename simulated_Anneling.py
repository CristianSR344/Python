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

def crear_solucion(matriz):
    lugares = list(range(1, len(matriz)))  # Excluye el punto de inicio (0)
    random.shuffle(lugares)
    return [0] + lugares + [0]   # Empieza y termina en 0

def simulated_annealing(matriz, temp_inicial, temp_final, coef_enfriamiento):
    #Realiza la búsqueda de la mejor solución utilizando el algoritmo de enfriamiento simulado.
    T = temp_inicial
    Tf = temp_final
    S = crear_solucion(matriz)
    ES = calcular_energia(S, matriz)
    Smejor = S[:]
    ESmejor = ES
    cont=1
    temp=[]
    while T > Tf:
        n=1
        while n<=300: 
            # Se perturba la solución actual intercambiando dos lugares en la ruta
            Snew = S[:]
            a, b = random.sample(range(1, len(Snew) - 1), 2)  # Elige dos puntos para intercambiar, sin incluir el primero y el último (0)
            Snew[a], Snew[b] = Snew[b], Snew[a]
            
            ESnew = calcular_energia(Snew, matriz)
            
            
            diferencia = ESnew - ES

            # Si la nueva solución es mejor, o se acepta una peor con cierta probabilidad para evitar mínimos locales
            if diferencia < 0:
                S = Snew
                ES = ESnew
                temp.append([cont,ESnew])
                # Si la nueva solución es la mejor hasta el momento, se actualiza Smejor y ESmejor
                if ES < ESmejor:
                    Smejor = S[:]
                    ESmejor = ES
                    
            else:
                probabilidad=math.exp(-diferencia / T) 
                if probabilidad> random.random():
                    S=Snew
                    ES=ESnew 
                    temp.append([cont,ESnew])   
            n+=1
            cont+=1

        # Se enfría la temperatura según la tasa de enfriamiento
        T *= coef_enfriamiento 
         
    with open('listas.csv', 'w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(temp)
        archivo.write('\n')   
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
        
    avg=avg/30
    
simulated_annealing(cost_matriz, temp_inicial, temp_final, coef_enfriamiento)

