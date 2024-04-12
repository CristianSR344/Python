# Lista de elementos
mi_lista = ['manzana', 'banana', 'cereza']

# Abrir archivo en modo escritura
archivo = open('mi_lista.txt', 'w')

# Escribir cada elemento de la lista en una nueva línea
archivo.write(str(mi_lista))

# Cerrar el archivo
archivo.close()