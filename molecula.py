import random

def calcular_energia(solucion, matriz):
    # Calcula la energía total de la solución basada en la matriz de costos.
    distancia = 0
    for i in range(len(solucion) - 1):
        distancia+= matriz[solucion[i]][solucion[i + 1]]
    return distancia


def ineff_coll_on_wall(molecula, buffer, matriz_costos, KE_perdida_min, KE_perdida_max):
    """
    Ineffective collision on the wall.
    Parameters:
        molecula (dict): A dictionary representing the molecule with keys 'perfil', 'PE', 'KE'.
        buffer (float): The central energy buffer.
        matriz_costos (list of list of int): Cost matrix to calculate potential energy.
        KE_perdida_min (float): Minimum kinetic energy loss rate.
        KE_perdida_max (float): Maximum kinetic energy loss rate.
    Returns:
        dict: Updated molecule with new profile, PE, and KE.
        float: Updated buffer.
    """

    # Obtener el perfil actual de la molécula y calcular el vecindario (nueva estructura)
    perfil_actual = molecula['perfil']
    perfil_nuevo = perfil_actual[:]  # Copia del perfil actual para modificar
    random.shuffle(perfil_nuevo)  # Obtener un vecindario aleatorio (nueva estructura)

    # Calcular la nueva energía potencial PEw'
    PEw_nueva = calcular_energia(perfil_nuevo, matriz_costos)

    # Verificar la condición de colisión ineficaz contra la pared
    PEw_actual = molecula['PE']
    KEw_actual = molecula['KE']

    if PEw_actual + KEw_actual >= PEw_nueva:
        # Obtener un valor q aleatorio en el intervalo [KE_perdida_min, 1]
        q = random.uniform(KE_perdida_min, KE_perdida_max)
        
        # Calcular la nueva energía cinética KEw'
        KEw_nueva = (PEw_actual + KEw_actual - PEw_nueva) * q
        
        # Actualizar el buffer
        buffer += (PEw_actual + KEw_actual - PEw_nueva) * (1 - q)
        
        # Actualizar el perfil de la molécula y sus energías PE y KE
        molecula['perfil'] = perfil_nuevo
        molecula['PE'] = PEw_nueva
        molecula['KE'] = KEw_nueva

    return molecula, buffer

# Ejemplo de uso:
# Definir la matriz de costos (ya proporcionada en tu código original)
cost_matriz = [
    [-1, 513, 507, 1190, 1100, 1150, 1280, 1230, 1120, 1270, 1030, 1000, 962],
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
    [938, 958, 877, 850, 787, 773, 809, 273, 165, 315, 162, 50, -1]
]

# Definir una molécula inicial y el buffer
molecula = {
    'perfil': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0],
    'PE': calcular_energia([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0], cost_matriz),
    'KE': 1000  # Ejemplo de energía cinética inicial
}
buffer = 0.0

# Parámetros de la colisión ineficaz
KE_perdida_min = 0.1
KE_perdida_max = 1.0

# Ejecutar la colisión ineficaz contra la pared
molecula_actualizada, buffer_actualizado = ineff_coll_on_wall(molecula, buffer, cost_matriz, KE_perdida_min, KE_perdida_max)

# Imprimir resultados
print("Molécula actualizada:", molecula_actualizada)
print("Buffer actualizado:", buffer_actualizado)

