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

def contra_pared(S, buffer,KEL):
    # Obtener una nueva estructura vecina aleatoria
    index=next(iter(S))

    Snew = S[index][:]
    random.shuffle(Snew)

    
    # Calcular la energía potencial de la nueva estructura
    EPnew = calcular_energia(Snew, cost_matriz)
    
    # Crear un nuevo individuo con la estructura vecina
    new = {index: Snew, 'EP': EPnew, 'EK': 0}
    
    # Verificar si la colisión ineficaz permite el cambio
    if S['EP'] + S['EK'] >= new['EP']:
        q = random.uniform(KEL, 1)  
        KEnew = (S['EP'] + S['EK'] - new['EP']) * q
        buffer += (S['EP'] + S['EK'] - new['EP']) * (1 - q)
        print(f"{S}+1")
        # Actualizar la estructura y energías del individuo
        S=Snew
        

        
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
    print (S)
    contra_pared(S,buffer,KEL)
    print (S)
    
    
    
    
        
ejecutar(matriz=cost_matriz)