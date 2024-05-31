import random
import math

cost_matriz= [
    [-1, 2500, 3000, 8500, 7900, 8200, 9100, 7800, 5600, 10000, 7100, 7300, 7000, 12000, 15000, 8000, 9500, 9900, 11000],
    [2500, -1, 1500, 7000, 6800, 6900, 8500, 8400, 4500, 8900, 5100, 5000, 5200, 13000, 14000, 7500, 8600, 9000, 10500],
    [3000, 1500, -1, 6700, 6400, 6500, 8000, 8300, 4200, 8600, 4800, 4700, 4800, 12500, 13500, 7200, 8300, 8700, 10000],
    [8500, 7000, 6700, -1, 1500, 1000, 2500, 10000, 7900, 11000, 6000, 6100, 5900, 7000, 8500, 1200, 3000, 3400, 4500],
    [7900, 6800, 6400, 1500, -1, 800, 2300, 9400, 7200, 10400, 5400, 5500, 5300, 7500, 9000, 1000, 3200, 3600, 4700],
    [8200, 6900, 6500, 1000, 800, -1, 2000, 9700, 7500, 10600, 5700, 5800, 5500, 7300, 8800, 1100, 3100, 3500, 4600],
    [9100, 8500, 8000, 2500, 2300, 2000, -1, 10600, 8400, 11500, 6600, 6700, 6400, 9200, 10700, 2600, 3600, 4000, 5100],
    [7800, 8400, 8300, 10000, 9400, 9700, 10600, -1, 3500, 4000, 5200, 5300, 5500, 2000, 3500, 9000, 10600, 11000, 12000],
    [5600, 4500, 4200, 7900, 7200, 7500, 8400, 3500, -1, 4500, 2500, 2700, 2400, 5000, 6500, 7000, 8000, 8400, 9500],
    [10000, 8900, 8600, 11000, 10400, 10600, 11500, 4000, 4500, -1, 6600, 6700, 6900, 6000, 7000, 10500, 11500, 11900, 13000],
    [7100, 5100, 4800, 6000, 5400, 5700, 6600, 5200, 2500, 6600, -1, 800, 1000, 8200, 9500, 4500, 5700, 6100, 7200],
    [7300, 5000, 4700, 6100, 5500, 5800, 6700, 5300, 2700, 6700, 800, -1, 600, 8500, 9600, 4600, 5800, 6200, 7300],
    [7000, 5200, 4800, 5900, 5300, 5500, 6400, 5500, 2400, 6900, 1000, 600, -1, 8000, 9100, 4400, 5600, 6000, 7100],
    [12000, 13000, 12500, 7000, 7500, 7300, 9200, 2000, 5000, 6000, 8200, 8500, 8000, -1, 2000, 9500, 12000, 12500, 14000],
    [15000, 14000, 13500, 8500, 9000, 8800, 10700, 3500, 6500, 7000, 9500, 9600, 9100, 2000, -1, 11000, 13500, 14000, 15500],
    [8000, 7500, 7200, 1200, 1000, 1100, 2600, 9000, 7000, 10500, 4500, 4600, 4400, 9500, 11000, -1, 2500, 2900, 4000],
    [9500, 8600, 8300, 3000, 3200, 3100, 3600, 10600, 8000, 11500, 5700, 5800, 5600, 12000, 13500, 2500, -1, 500, 1600],
    [9900, 9000, 8700, 3400, 3600, 3500, 4000, 11000, 8400, 11900, 6100, 6200, 6000, 12500, 14000, 2900, 500, -1, 2100],
    [11000, 10500, 10000, 4500, 4700, 4600, 5100, 12000, 9500, 13000, 7200, 7300, 7100, 14000, 15500, 4000, 1600, 2100, -1]
]
lugares = [
    [0, "ITS"],
    [1, "SAMS"],
    [2, "Galerías Saltillo"],
    [3, "UAdC"],
    [4, "Home Depot"],
    [5, "UANE Saltillo"],
    [6, "Tupy Saltillo"],
    [7, "Roller Rock Saltillo"],
    [8, "Al Super V. Carranza"],
    [9, "Club Deportivo San Isidro Saltillo"],
    [10, "Christus Muguerza Saltillo"],
    [11, "Costco Saltillo"],
    [12, "Villa Ferré Saltillo"],
    [13, "Parque El Chapulín"],
    [14, "Museo del Desierto"],
    [15, "Estadio Olímpico"],
    [16, "Plaza de Armas"],
    [17, "Biblioteca Central del Estado"],
    [18, "Universidad La Salle Saltillo (ULSA)"]
]


def mutacion(individuo,poblacion,matriz):
    index = next(iter(individuo))
    length = len(poblacion)
    Snew = individuo[index][1:-1]
    a, b = random.sample(range(1, len(Snew) - 1), 2)  # Elige dos puntos para intercambiar, sin incluir el primero y el último (0)
    Snew[a], Snew[b] = Snew[b], Snew[a]
    Snew = [0] + Snew + [0]
    Emut=calcular_energia(Snew,matriz)
    mutacion={length:Snew,'EP':Emut,'EK':0}
    return  mutacion

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
    mejor_individuo =poblacion[mejor_individuo].copy()
    return mejor_individuo


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

    nuevo_individuo1 = a[:]
    nuevo_individuo2 = b[:]
    

    
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

    EPnew1 = calcular_energia(Snew1, matriz)
    EPnew2 = calcular_energia(Snew2, matriz)

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
        mejor=selecciona_el_mejor_individuo(poblacion, matriz)
        individuo=random.choice(poblacion)
        #Se combinan los individuos
        Snew1,Snew2=combinar(mejor,individuo)
        #Calcular la energia de los individuos
        ESnew1=calcular_energia(Snew1,matriz)
        ESnew2=calcular_energia(Snew2,matriz)
        length=len(poblacion)
        new1={length:Snew1,'EP':ESnew1,'EK':0}
        new2={length+1:Snew2,'EP':ESnew2,'EK':0}
        new1,buffer= perturbar_con_reaccion_quimica(new1, buffer,poblacion,KEL,matriz)
        new2,buffer= perturbar_con_reaccion_quimica(new2, buffer,poblacion,KEL,matriz)
        
        poblacion.append(new1)
        poblacion.append(new2)  
        #Compara para encontrar el mejor individuo
        if(new1['EP']>new2['EP']):
            mejor_actual=new1.copy()
        else:
            mejor_actual=new2.copy()
        
        if  random.random()<tasa_mutacion:
             mutar=mutacion(mejor_actual,poblacion,matriz)
             poblacion.append(mutar)
        

        
        #Acepta al mejor actual como el mejor
        if mejor_actual['EP']<mejor['EP']:
            mejor=mejor_actual.copy()
         
        n+=1
     
    
    return mejor

tasa_mutacion = 0.1
tamano_poblacion = 100
num_generaciones = 300


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
        mejor_ruta= algoritmo_genetico(cost_matriz, num_generaciones, tamano_poblacion, tasa_mutacion)
        print(mejor_ruta)
        temp=[mejor_ruta, mejor_ruta['EP']]
        mu.append(temp)
        avg+=mejor_ruta['EP']
        
    avg=avg/30
    print(avg)


# mejor_ruta = algoritmo_genetico(cost_matriz, num_generaciones, tamano_poblacion, tasa_mutacion)

# print(mejor_ruta,mejor_ruta['EP'])
muestra()