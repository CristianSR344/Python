
import random

# Definir la matriz de costos
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

def mutacion(individuo):
    nuevo = individuo[1:][:-1]  # Excluye el punto de inicio (0)
    random.shuffle(nuevo)
    return [0] + nuevo + [0] 

def algoritmo_genetico(matriz, num_generaciones, tamano_poblacion, tasa_mutacion):
    poblacion = crear_poblacion_inicial(tamano_poblacion, matriz)
    n=0
    while n<num_generaciones:
        mejor,Emejor=selecciona_el_mejor_individuo(poblacion, matriz)
        individuo=random.choice(poblacion)
        
        #Se combinan los individuos
        Snew1,Snew2=combinar(mejor,individuo)
        

        #Calcular la energia de los individuos
        ESnew1=calcular_energia(Snew1,matriz)
        ESnew2=calcular_energia(Snew2,matriz)
        
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
        Emejor_actual=calcular_energia(mejor_actual,matriz)
        
        #Acepta al mejor actual como el mejor
        if Emejor_actual<Emejor:
            mejor, Emejor=mejor_actual,Emejor_actual
         
  
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
        mejor_ruta=nombres(mejor_ruta,lugares)
        print(mejor_ruta,mejor_costo)
        temp=[mejor_ruta, mejor_costo]
        mu.append(temp)
        avg+=mejor_costo
        
    avg=avg/30
    print(avg)


# mejor_ruta, mejor_costo = algoritmo_genetico(cost_matriz, num_generaciones, tamano_poblacion, tasa_mutacion)
# mejor_ruta=nombres(mejor_ruta,lugares)
# print(mejor_ruta,mejor_costo)

muestra()

