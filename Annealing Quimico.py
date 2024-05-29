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

def perturbar_con_reaccion_quimica(S,buffer,poblacion,KEL,matriz):
    ran=random.randint(1,4)
    if ran==1:
        S,buffer=contra_pared(S,buffer,KEL)
    elif ran==2:
        S,buffer=descomposicion(S, buffer,KEL,poblacion,matriz)
    elif ran==3:
        ran2=random.randrange(0,len(poblacion)-1) 
        S2=poblacion[ran2]
        intramolecular_ineficaz(S,S2, buffer,KEL,poblacion,matriz)
    elif ran==4:
        ran2=random.randrange(0,len(poblacion)-1) 
        S2=poblacion[ran2]
        sintesis(S,S2, buffer,KEL,poblacion,matriz)
    return S,buffer

def contra_pared(S, buffer,KEL):
    # Obtener una nueva estructura vecina aleatoria
    index=next(iter(S))

    # Obtener la estructura actual y mantener el primer y último elemento como 0
    Snew = S[index][1:-1]  # Excluir el primer y último elemento (ambos 0)
    random.shuffle(Snew)  # Barajar los elementos intermedios
    Snew = [0] + Snew + [0]  # Volver a agregar 0 al inicio y al final
    
    # Calcular la energía potencial de la nueva estructura
    EPnew = calcular_energia(Snew, cost_matriz)
    # Crear un nuevo individuo con la estructura vecina
    new = {index: Snew, 'EP': EPnew, 'EK': 0}

    
    # Verificar si la colisión ineficaz permite el cambio
    if S['EP'] + S['EK'] >= new['EP']:
        q = random.randrange(KEL, 1)  
        KEnew = (S['EP'] + S['EK'] - new['EP']) * q
        buffer += (S['EP'] + S['EK'] - new['EP']) * (1 - q)
        # Actualizar la estructura y energías del individuo
        S[index] = new[index][:]
        S['EP'] = new['EP']
        S['EK'] = KEnew
    return S, buffer

def intramolecular_ineficaz(S1,S2, buffer,KEL,poblacion,matriz):
    length = len(poblacion)
    # Obtener el índice de los individuos en S
    index1 = next(iter(S1))
    index2=next(iter(S2))
    

    # Obtener la estructura actual y mantener el primer y último elemento como 0
    Snew1 = S1[index1][1:-1]  # Excluir el primer y último elemento (ambos 0)
    random.shuffle(Snew1)  # Barajar los elementos intermedios
    Snew1 = [0] + Snew1 + [0]  # Volver a agregar 0 al inicio y al final
    

    # Obtener la estructura actual y mantener el primer y último elemento como 0
    Snew2 = S2[index2][1:-1]  # Excluir el primer y último elemento (ambos 0)
    random.shuffle(Snew2)  # Barajar los elementos intermedios
    Snew2 = [0] + Snew2 + [0]  # Volver a agregar 0 al inicio y al final
    
    #Obtener energia de los individuos
    EPnew1=calcular_energia(Snew1,matriz)
    EPnew2=calcular_energia(Snew2,matriz)
    
    new1={'i1':Snew1, 'EP': EPnew1, 'EK':0}
    new2={'i2':Snew2, 'EP': EPnew2, 'EK':0}
    
    
    
    temp=(S1['EP']+S2['EP']+S1['EK']+S2['EK'])-(new1['EP']+new2['EP'])
    
    if temp>=0:
        p=random.randrange(0,1)
        EKnew1=temp*p
        EKnew2=temp * (1-p)
        S1[index1]=new1['i1'][:]
        S1['EP']=new1['EP']
        S1['EK']=new1['EK']
        S2[index2]=new2['i2'][:]
        S2['EP']=new2['EP']
        S2['EK']=new2['EK']

     
 
    if S1['EP']>S2['EP']:   
        return S1, buffer
    
    else:
        return S2,buffer

def descomposicion(S, buffer,KEL,poblacion,matriz):

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

    return S, buffer
    
def sintesis(S1,S2, buffer,KEL,poblacion,matriz):
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

def simulated_annealing(matriz, temp_inicial, temp_final, coef_enfriamiento):
    #Realiza la búsqueda de la mejor solución utilizando el algoritmo de enfriamiento simulado.
    T = temp_inicial
    Tf = temp_final
    individuos=100
    poblacion=crear_poblacion_inicial(individuos,matriz) 
    ran=random.randrange(0,individuos-1)   
    S=poblacion[ran]
    ES=S['EP']
    Etotal=energia_total(poblacion)
    buffer=Etotal/0.5
    Smejor = S
    ESmejor=S['EP']
    while T > Tf:
         n=1
         while n<=100: 
             KEL=random.randrange(0,1)
             Snew,buffer = perturbar_con_reaccion_quimica(S, buffer,poblacion,KEL,matriz)
             ESnew=Snew['EP'] 
             diferencia = ESnew - ES
             # Si la nueva solución es mejor, o se acepta una peor 
             if diferencia < 0:
                 S = Snew
                 ES = Snew['EP']
                 # Si la nueva solución es la mejor hasta el momento, se actualiza Smejor y ESmejor
                 if ES < ESmejor:
                     Smejor = S
                     ESmejor = S['EP']

                    
             else:
                 probabilidad=math.exp(-diferencia / T) 
                 if probabilidad> random.random():
                     S=Snew
                     ES=S['EP']

             n+=1

         # Se enfría la temperatura según la tasa de enfriamiento
         T *= coef_enfriamiento 
          
    return Smejor

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
        best_solucion = simulated_annealing(cost_matriz, temp_inicial, temp_final, coef_enfriamiento)
        temp=[best_solucion]
        mu.append(temp)
        avg+=best_solucion['EP']
        print (best_solucion)
    avg=avg/30
    print(avg)
    
# best_solucion, best_energy = simulated_annealing(cost_matriz, temp_inicial, temp_final, coef_enfriamiento)
# print (best_solucion, best_energy)
muestra()

# simulated_annealing(cost_matriz, temp_inicial, temp_final, coef_enfriamiento)