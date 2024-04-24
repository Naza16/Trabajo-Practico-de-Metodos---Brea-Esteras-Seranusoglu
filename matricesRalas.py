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
        m : int = Idx[0] # Filas
        n : int = Idx[1] # Columnas
     
        # Si la columna no esta en la lista enlazada, o no hay una lista asociado a la fila m devuelve 0.
        valor_posicion = 0
        
        # Veo si la fila n tiene una lista enlazada
        if m in self.filas:

            #Obtengo la lista enlazada de la fila
            fila = self.filas[m]

            # Recorro la lista enlazada. Si hay un elemento en la columna n,
            # cambio el valor de valor_posicion.
            nodoActual = fila.raiz
            while not nodoActual == None:
                if nodoActual.valor[0] == n:
                    valor_posicion = nodoActual.valor[1]  
                nodoActual = nodoActual.siguiente 

        return valor_posicion

    def __setitem__( self, Idx, v ):
        # Si v = 0, no hay que agregarlo a la matriz rala.
        if v == 0:
            return 
        

        # Esta funcion implementa la asignacion durante indexacion ( Idx es una tupla (m,n) ) -> A[m,n] = v
        m : int = Idx[0]
        n : int = Idx[1]

        # Si la fila no tiene una lista enlazada, creamos una y le ponemos como raiz el nodo (n, v)
        if m not in self.filas:
            self.filas[m] = ListaEnlazada()
            self.filas[m].insertarFrente((n, v))
            
        else:
            lista = self.filas[m]
            nodoAnterior = lista.raiz

            # Si la columna del elemento esta antes de la primera columna de la lista enlazada
            if n < nodoAnterior.valor[0]:
                lista.insertarFrente((n,v))
                return 
            
            # Si la columna del elemento esta en la primera columna de la lista enlazada, reemplaza valor.
            elif n == nodoAnterior.valor[0]:
                nodoAnterior.valor = (n,v)
                return
            
            nodoActual: ListaEnlazada.Nodo = nodoAnterior.siguiente

            # Recorro la lista enlazada
            while (nodoActual != None):
                
                # Si el elemento esta entre las columnas del nodoAnterior y el nodoActual, lo
                # agrega a la lista despues de nodoAnterior 
                if(nodoAnterior.valor[0] < n < nodoActual.valor[0]):
                    lista.insertarDespuesDeNodo((n,v),nodoAnterior)
                    return
                
                # Si el elemento esta en la columna de nodo actual, reemplaza el valor.
                elif (nodoActual.valor[0] == n):
                    nodoActual.valor = (n,v)
                    return

                nodoAnterior = nodoActual
                nodoActual = nodoActual.siguiente

            # Si la columna del elemento esta no aparecio mientras se recorria la lista
            # significa que tiene que estar al final. Entonces se la pushea a la lista enlazada.
            lista.push((n,v))

            
    def __mul__( self, k):
        # COMPLETAR:
        # Esta funcion implementa el producto matriz-escalar -> A * k
        nueva_matriz = MatrizRala(self.shape[0],self.shape[1])

        for i in range (len(self.filas)):
            lista = self.filas[i]
            nodoActual = lista.raiz

            while not nodoActual == None:
                columna,valor = nodoActual.valor
                nueva_matriz[i,columna] = valor*k
                nodoActual = nodoActual.siguiente

        return nueva_matriz
    
    def __rmul__( self, k ):
        # Esta funcion implementa el producto escalar-matriz -> k * A
        return self * k

    def __add__( self, other ):
        # Esta funcion implementa la suma de matrices -> A + B
        #Asumimos que las matrcies son del mismo tamaño 
        if(self.shape == other.shape):
            c= MatrizRala(self.shape[0],self.shape[1])
            for i in range(len(other.filas)):
                fila = other.filas[i]
                nodoActual = fila.raiz
                while not (nodoActual == None):
                    columna,valor = nodoActual.valor
                    c[i,columna]+=valor
                    nodoActual = nodoActual.siguiente

            for i in range(len(self.filas)):
                fila = self.filas[i]
                nodoActual = fila.raiz
                while not (nodoActual == None):
                    columna,valor = nodoActual.valor
                    c[i,columna]+=valor
                    nodoActual = nodoActual.siguiente
            return c
        
        else:
            raise ValueError("Las matrices son de distintos tamaños")

    def __sub__( self, other ):
        #Esta funcion implementa la resta de matrices (pueden usar suma y producto) -> A - B
        return self + ((-1)*other)

    def __matmul__( self, other ):
        # Esta funcion implementa el producto matricial (notado en Python con el operador "@" ) -> A @ B
        if self.shape[1] != other.shape[0]:
            raise ValueError("No se pueden multiplicar las matrices")
        m = MatrizRala(self.shape[0], other.shape[1])
        for f in range(len(self.filas)):
            fila=self.filas[f]
            nodo_actual=fila.raiz
            while not nodo_actual ==None:
                col_a,val=nodo_actual.valor
                for col_b in range(other.shape[1]):
                    valor_nuevo=val*other[col_a,col_b]
                    m[f,col_b]+=valor_nuevo
                nodo_actual=nodo_actual.siguiente
        return m

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

A = MatrizRala(3,2)

A[0,1] = 1
A[0,0] =  2
A[1,1] = 1
A[1,0] =0
A[2,0] = 3
A[2,1] = 3

B = MatrizRala(2,3)

B[0,1] = 3
B[1,0] = 1
B[0,0] = 1
B[1,1] = 1
B[0,2] = 2
B[1,2] = -1

C = A@B
print(C)

