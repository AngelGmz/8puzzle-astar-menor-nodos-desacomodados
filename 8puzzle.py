from ast import While
import copy
'''
Reglas
-La casilla vacía puede intercambiarse sólo con sus casillas abyacentes;
Si la casilla vacía se encuentra en el centro, puede intercambiarce en forma de cruz.
-La casilla vacía nopuede intercambiar con casillas diagonales, es decir solo puede moverce de manera vertical
y horizontal
'''


from math import dist
import re
from tkinter import Y


class Estado:
    h = None
    g= None
    p = None
    f = None
    def __init__(self, matriz) -> None:
        self.matriz = matriz

    def __str__(self) -> str:
        text = ''
        for y in range(0, 3):
            for x in range(0, 3):
                text += str(self.matriz[y][x]) + ' '
            text += '\n'
        return text
    def imprimir_matriz(self):
        for y in range(0, 3):
            for x in range(0, 3):
                print(self.matriz[y][x], end=" ")
            print(' ')

class Coordenada:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
    def __str__(self) -> str:
        return 'y: ' + str(self.y) + ' x:' + str(self.x)

class Juego:

    def __init__(self, e_inicial, e_estado_final) -> None:
        self.estado_inicial = Estado(e_inicial)
        self.estado_final = Estado(e_estado_final)
        self.estado_actual = copy.deepcopy(self.estado_inicial)
        self.lista_cerrada = []
        self.lista_abierta = []
        self.lista_jugadas = []
        self.lista_camino = []
        #self.estado_actual = self.estado_actual

    def buscar_coordenada_n(self, estado, numero):
        for y in range(0, 3):
            for x in range(0, 3):
                if estado.matriz[y][x] == numero:
                    return Coordenada(y, x )

    def buscar_matriz_en_lista(self, matriz, lista):
        flag = False
        for l in lista:
            if self.comparar_matrices(matriz, l.matriz):
                flag = True
        return flag
        
    def obtener_estados_posibles(self, estado):
        nodo_actual = self.buscar_coordenada_n(estado, 0)
        #print(nodo_actual.x)
        #-----
        # No está funcionando el not in, es decir siempre lo valida como verdadero
        #-----
        #arriba
        if nodo_actual.y-1 < len(estado.matriz) and nodo_actual.x < len(estado.matriz) and  nodo_actual.y -1 >= 0 and nodo_actual.x >= 0:
            aux = copy.deepcopy(estado)
            aux.matriz[nodo_actual.y][nodo_actual.x] = estado.matriz[nodo_actual.y-1][nodo_actual.x]
            aux.matriz[nodo_actual.y-1][nodo_actual.x] = 0
            #if not self.comparar_matrices(aux.matriz, self.lista_cerrada[-1].matriz):
            if not self.buscar_matriz_en_lista(aux.matriz, self.lista_cerrada):
                self.lista_jugadas.append(aux)
        #abajo
        if nodo_actual.y+1 < len(estado.matriz) and nodo_actual.x < len(estado.matriz) and  nodo_actual.y +1 >= 0 and nodo_actual.x >= 0:
            aux = copy.deepcopy(estado)
            aux.matriz[nodo_actual.y][nodo_actual.x] = estado.matriz[nodo_actual.y+1][nodo_actual.x]
            aux.matriz[nodo_actual.y+1][nodo_actual.x] = 0
            #if not self.comparar_matrices(aux.matriz, self.lista_cerrada[-1].matriz):
            if not self.buscar_matriz_en_lista(aux.matriz, self.lista_cerrada):
                self.lista_jugadas.append(aux)
        #izqueirda
        if nodo_actual.y < len(estado.matriz) and nodo_actual.x-1 < len(estado.matriz) and  nodo_actual.y >= 0 and nodo_actual.x-1 >= 0:
            aux = copy.deepcopy(estado)
            aux.matriz[nodo_actual.y][nodo_actual.x] = estado.matriz[nodo_actual.y][nodo_actual.x-1]
            aux.matriz[nodo_actual.y][nodo_actual.x-1] = 0 
            #if not self.comparar_matrices(aux.matriz, self.lista_cerrada[-1].matriz):
            if not self.buscar_matriz_en_lista(aux.matriz, self.lista_cerrada):
                self.lista_jugadas.append(aux)
        #detecha
        if nodo_actual.y < len(estado.matriz) and nodo_actual.x+1 < len(estado.matriz) and  nodo_actual.y >= 0 and nodo_actual.x+1 >= 0:
            aux = copy.deepcopy(estado)
            aux.matriz[nodo_actual.y][nodo_actual.x] = estado.matriz[nodo_actual.y][nodo_actual.x+1]
            aux.matriz[nodo_actual.y][nodo_actual.x+1] = 0
            #if not self.comparar_matrices(aux.matriz, self.lista_cerrada[-1].matriz):
            if not self.buscar_matriz_en_lista(aux.matriz, self.lista_cerrada):
                self.lista_jugadas.append(aux)

    def numero_posiciones_desordenados(self, matriz, matriz_final):
        contador = 0
        for y in range(0, len(matriz)):
            for x in range(0, len(matriz)): 
                if matriz[y][x] != matriz_final[y][x]:
                    contador += 1
        return contador

    def dist_manhattan(self, num, estado):
        coordenada_inicial = self.buscar_coordenada_n(estado, num)
        coordenada_final =   self.buscar_coordenada_n(self.estado_final, num)
        return abs( coordenada_inicial.x - coordenada_final.x   ) + abs(  coordenada_inicial.y - coordenada_final.y  )

    def econtrar_estado_de_menor_peso(self, estados):
        menor = estados[0]
        for e in estados:
            if e.f < menor.f:
                menor = e
        return menor
        
    def comparar_matrices(self, m1, m2):
        for y in range(0, 3):
            for x in range(0, 3): 
                if m1[y][x] != m2[y][x]:
                    return False
        return True

    def imprimir_lista(self, matriz):
        for e in matriz:
            print('-----')
            e.imprimir_matriz()
            print('-----')

    def llenar_lista_de_predecesores(self, cerrada):
        actual = cerrada[-1]
        self.lista_camino.append(actual)
        while actual.p != None:
            self.lista_camino.append(actual.p)
            actual = actual.p
        

    def buscar_ruta(self):
        
        if self.estado_inicial != self.estado_final:
            self.estado_actual.g = 0
            self.estado_actual.h = self.numero_posiciones_desordenados(self.estado_actual.matriz, self.estado_final.matriz)
            self.lista_cerrada.append(self.estado_actual)
            while not self.comparar_matrices( self.estado_actual.matriz , self.estado_final.matriz):
                self.obtener_estados_posibles(self.estado_actual)
                for e in self.lista_jugadas:
                    e.g = self.estado_actual.g + 1 
                    e.h = self.numero_posiciones_desordenados(e.matriz, self.estado_final.matriz)
                    e.f = e.g + e.h
                    e.p = self.estado_actual
                    self.lista_abierta.append(e)
                self.estado_actual = self.econtrar_estado_de_menor_peso(self.lista_abierta)
                self.lista_abierta.pop( self.lista_abierta.index(self.estado_actual))
                self.lista_cerrada.append(self.estado_actual)
                self.lista_jugadas.clear()
            print('Numero de Nodos abiertos ', len(self.lista_abierta) + len(self.lista_cerrada))
            self.llenar_lista_de_predecesores(self.lista_cerrada)
            self.lista_camino = self.lista_camino[::-1]
            print('Camino mas corto',len(self.lista_camino))
            print("lista Camino")
            self.imprimir_lista(self.lista_camino)


        else:
            print('El nodo Inicial es el mismo que el final')
            #está resuleto solo mostrar el mismo cuadro
        
        print('Termina Ejecución')

if __name__ == '__main__':
    estado_inicial = [[2, 8, 3], [1, 6, 4], [7, 0, 5]]
    estado_final = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
    j = Juego(estado_inicial, estado_final)
    j.buscar_ruta()