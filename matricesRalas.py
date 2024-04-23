# IMPORTANTE: Para importar estas clases en otro archivo (que se encuentre en la misma carpeta), escribir:
# from matricesRalas import MatrizRala, GaussJordan 

from typing import Dict

class ListaEnlazada:
    def __init__( self ):
        self.raiz = None
        self.longitud = 0
        self.current = self.Nodo(None, self.raiz)

    def insertarFrente( self, valor ):
        # Inserta un elemento al inicio de la lista
        if len(self) == 0:
            return self.push(valor)    
    
        nuevoNodo = self.Nodo( valor, self.raiz )
        self.raiz = nuevoNodo
        self.longitud += 1

        return self

    def insertarDespuesDeNodo( self, valor, nodoAnterior ):
        # Inserta un elemento tras el nodo "nodoAnterior"
        nuevoNodo = self.Nodo( valor, nodoAnterior.siguiente)
        nodoAnterior.siguiente = nuevoNodo

        self.longitud += 1
        return self

    def push( self, valor ):
        # Inserta un elemento al final de la lista
        if self.longitud == 0:
            self.raiz = self.Nodo( valor, None )
        else:      
            nuevoNodo = self.Nodo( valor, None )
            ultimoNodo = self.nodoPorCondicion( lambda n: n.siguiente is None )
            ultimoNodo.siguiente = nuevoNodo

        self.longitud += 1
        return self
    
    def pop( self ):
        # Elimina el ultimo elemento de la lista
        if len(self) == 0:
            raise ValueError("La lista esta vacia")
        elif len(self) == 1:
            self.raiz = None
        else:
            anteUltimoNodo = self.nodoPorCondicion( lambda n: n.siguiente.siguiente is None )
            anteUltimoNodo.siguiente = None
        
        self.longitud -= 1

        return self

    def nodoPorCondicion( self, funcionCondicion ):
        # Devuelve el primer nodo que satisface la funcion "funcionCondicion"
        if self.longitud == 0:
            raise IndexError('No hay nodos en la lista')
        
        nodoActual = self.raiz
        while not funcionCondicion( nodoActual ):
            nodoActual = nodoActual.siguiente
            if nodoActual is None:
                raise ValueError('Ningun nodo en la lista satisface la condicion')
            
        return nodoActual
        
    def __len__( self ):
        return self.longitud

    def __iter__( self ):
        self.current = self.Nodo( None, self.raiz )
        return self

    def __next__( self ):
        if self.current.siguiente is None:
            raise StopIteration
        else:
            self.current = self.current.siguiente
            return self.current.valor
    
    def __repr__( self ):
        res = 'ListaEnlazada([ '

        for valor in self:
            res += str(valor) + ' '

        res += '])'

        return res

    class Nodo:
        def __init__( self, valor, siguiente ):
            self.valor = valor
            self.siguiente = siguiente

class MatrizRala:
    def __init__( self, M, N ):
        self.filas : Dict[int, ListaEnlazada] = {}
        self.shape = (M, N)


    def __getitem__( self, Idx ):
        # Esta funcion implementa la indexacion ( Idx es una tupla (m,n) ) -> A[m,n]
        M : int = Idx[0]
        N : int = Idx[1]
        if (M < 0 or N < 0):
            return IndexError("El elemento pasado por parametro, no coincide con la fila y la columna de la matriz")
        fila = self.filas[M]
    
        #Verifico si coincide la columna que es pasada por el Idx
        def condicion_columnas(nodo:ListaEnlazada.Nodo):
            columna = nodo.valor[0]
            if N == columna:
                return True
            else:
                return False            
        
        nodo_posicion = fila.nodoPorCondicion(condicion_columnas)
        #Devolvemos el elemento que se halla en esa posicion
        return nodo_posicion.valor[1]

    def __setitem__( self, Idx, v ):
        # Esta funcion implementa la asignacion durante indexacion ( Idx es una tupla (m,n) ) -> A[m,n] = v
        m : int = Idx[0]
        n : int = Idx[1]
        if m not in self.filas:
            self.filas[m] = ListaEnlazada()
            self.filas[m].insertarFrente((n, v))
            return 
        else:
            lista = self.filas[m]
            nodoActual = lista.raiz
            if lista.longitud == 1 :
                columna = nodoActual.valor[0]
                if (columna < n):
                    lista.insertarDespuesDeNodo((n,v),nodoActual)
                elif (columna > n):
                    lista.insertarFrente((n,v))
                else:
                    nodoActual.valor = (n,v)
            else: 
                columna_actual = nodoActual.valor[0]
                if n < columna_actual:
                    lista.insertarFrente((n,v))
                    return 
                elif n == columna_actual:
                    nodoActual.valor = (n,v)
                    return
                nodoAnterior: ListaEnlazada.Nodo = nodoActual
                nodoActual: ListaEnlazada.Nodo = nodoActual.siguiente
                while (nodoActual != None):
                    if(nodoAnterior.valor[0] < n < nodoActual.valor[0]):
                        lista.insertarDespuesDeNodo((n,v),nodoAnterior)
                        return
                    elif (nodoActual.valor[0] == n):
                        nodoActual.valor = (n,v)
                        return
                    else:
                        nodoAnterior = nodoActual
                        nodoActual = nodoActual.siguiente
                lista.push((n,v))
            
    def __mul__( self, k ):
        # COMPLETAR:
        # Esta funcion implementa el producto matriz-escalar -> A * k
        pass
    
    #CONSULTAR
    def __rmul__( self, k ):
        # Esta funcion implementa el producto escalar-matriz -> k * A
        return self * k

    def __add__( self, other ):
        # COMPLETAR:
        # Esta funcion implementa la suma de matrices -> A + B
        pass
    
    def __sub__( self, other ):
        #Esta funcion implementa la resta de matrices (pueden usar suma y producto) -> A - B
        #COMPLETAR
        pass

    def __matmul__( self, other ):
        # COMPLETAR:
        # Esta funcion implementa el producto matricial (notado en Python con el operador "@" ) -> A @ B
        pass  

    #Consultar la forma de impresion
    def __repr__( self ):
        res = 'MatrizRala([ \n'
        for i in range( self.shape[0] ):
            res += '    [ '
            for j in range( self.shape[1] ):
                res += str(self[i,j]) + ' '
            
            res += ']\n'

        res += '])'

        return res

def GaussJordan( A, b ):
    # Hallar solucion x para el sistema Ax = b
    # Devolver error si el sistema no tiene solucion o tiene infinitas soluciones, con el mensaje apropiado
    pass

A = MatrizRala(4,4)
A.__setitem__((1,1),100)
print(A.filas)
A.__setitem__((1,2),3)
print(A.filas)
A.__setitem__((1,0),489765)
print(A.filas)
print(A[1,1])
print(A[1,2])
print(A[1,0])
