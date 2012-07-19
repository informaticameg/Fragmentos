#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Informática MEG <contacto@informaticameg.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from database import Database
from snippet import Snippet


class SnippetManagerCouch:
    ''' Clase que hace de wrapper entre las clases
    de la logica del programa, con la clase Fragmentos'''

    def __init__(self):
        
        # class instances
        
        # private instances
        self.__BD = None
        # diccionario con todas las instancia de objeto Snippet
        self.__Snippets = None
        # objeto snippet mostrado actualmente en GUI
        self.__SnippetActual = None # Snippet
        
        # esta variable, se utilizara para saber si la instancia de 
        # snippetmanager se creo correctamente con una bd determinada
        # o se creo vacia, indicando que no se puede realizar ninguna
        # operacion sobre la aplicacion 
        self.__estado = False
        
        # lista con las rutas de las base de datos
        # tanto las del pathdefault como del cfg file
        self.__AllPathDBs = []
#        self.loadAllPathDBs()
#        
#        # trae si existe, el valor de la bd a cargar por defecto
#        defaultBdName = self.__Configs.defaultBdName
#        if defaultBdName :          
#            # obtiene el indice de la ruta de la bd a cargarce 
#            pathBD = self.getPathBD(
#                                self.getIndexBdName(defaultBdName))
#            # crea la instancia de el catalogo en cuestion 
#            self.__BD = Database(pathBD)
#            
#            # instancia creada correctamente
#            self.__estado = True
#            
#        elif self.__AllPathDBs:
#            # sino, se carga la primer bd encontrada en la lista de bds
#            self.__BD = Database(
#                        self.getPathDB(0))
#        
#            # diccionario con todas las instancia de objeto Snippet
#            self.__Snippets = self.getAllSnippets()
#            
#            # instancia creada correctamente
#            self.__estado = True                    

##########################
## Metodos de instancia ##
##########################

    def agregarSnippet(self, datosSnippet):
        ''' Recibe un dicionario de los datos de lo que sera un nuevo
        snippet y lo agrega a la BD.'''
        
        # llama al metodo de bd para agregar un snippet, devolviendo
        # el resultado de la operacion como boolean y en caso de error, 
        # el mensaje del error.
        resultado, mensaje = self.__BD.agregarSnippet(datosSnippet)
        if resultado:
            # crea una instancia del nuevo snippet
            newSnippet = Snippet(datosSnippet, None)
            # agrega el nuevo snippet a los ya existentes
            self.__addNewSnippetToCollection(newSnippet)
            # retorna que la operacion fue exitosa, 
            #  y ningun mensaje de error
            return True, None
        else:
            # retorna que la operacion no fue exitosa, y 
            # el mensaje de error devuelto por bd
            return False,mensaje

    def eliminarSnippet(self, unSnippet):
        ''' Manda a eliminarSnippet de la Bd que
        borre el snippet segun su titulo y lenguaje.'''
        
        # llama al metodo de bd para eliminar un snippet
        # y devuelve un booleano con el resultado de la operacion.
        if self.__BD.eliminarSnippet(
            unSnippet.titulo, unSnippet.lenguaje):
                # quita del diccionario el snippet
                self.__Snippets.pop((unSnippet.lenguaje,
                                        unSnippet.titulo))
                # establece como actual snippet a None
                self.__SnippetActual = None
                return True
        else:
            return False

    def modificarSnippet(self, clave_spviejo, snippet_nuevo):
        ''' Actualiza el snippet cargado en memoria'''
        del self.__Snippets[clave_spviejo]
        self.__Snippets[
                (snippet_nuevo.lenguaje,snippet_nuevo.titulo)
                    ] = snippet_nuevo

    def newSnippet(self, spt):
        ''' Crea una instancia de snippet. '''
        nuevoSnippet = Snippet({
            'title':spt['title'],
            'language':spt['language'],
            'tags':','.join(spt['tags']),
            'contens':spt['contens'],
            'description':spt['description'],
            'creation':spt['creation'],
            'reference':spt['reference'],
            'modified':spt['modified'],
            'uploader':spt['uploader'],
            'starred':spt['starred']},
             None)
            
        # tupla que sera de clave en el diccionario de los snippets
        clave = (spt['language'],spt['title'])
        return (clave,nuevoSnippet)

#################
## Metodos Get ##
#################

    def getAllLenguajes(self):
        ''' Obtiene una lista de los lenguajes desde la bd.'''
        
        # obtiene desde la actual instancia de bd los lenguajes existentes 
        lenguajes = self.__BD.getLenguajes()
        lenguajes.sort()
        return lenguajes
    
    def getAllSnippets(self):
        ''' Obtiene los snippets desde la bd y carga en un diccionario
        los snippets en formato objeto Snippet().'''
        
        all = self.__BD.getAllSnippets()
        return dict([self.newSnippet(snippet) for snippet in all])

    def getLengsAndTitles(self,consulta=None, favorito = None):
        ''' Obtiene los snippets por lenguajes desde la bd.'''
        #~ tagsPresicion = bool(self.__DBUtils.configs.searchPresitionTags)
        tagsPresicion = False
        return self.__BD.getLengAndTitles(consulta, favorito, tagsPresicion)

    def getSnippetsCount(self):
        ''' Devuelve un entero con la cantidad de snippets cargados en la BD.'''
        return self.__BD.getSnippetsCount()

    def getPathDB(self, index):
        ''' Recupera de la lista de bds la ruta en el indice especificado.'''
        return self.__AllPathDBs[index]

#################
## Metodos Set ##
#################

    def setDB(self, pathBD, name):
        '''Crea una instancia de BD'''
        self.__BD = Database(pathBD,name)
        # se vuelven a reobtener los snippets desde esta nueva bd        
        self.__Snippets = self.getAllSnippets()

#if __name__ == '__main__':
#    s = SnippetManager()
#    s.setDB('http://192.168.1.5:5984/','sourcecode')
#    