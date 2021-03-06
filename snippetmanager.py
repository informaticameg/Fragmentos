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
from pathtools import PathTools

from sm_base import SnippetManagerBase


class SnippetManager (SnippetManagerBase):
    ''' Clase que hace de wrapper entre las clases
    de la logica del programa, con la clase Fragmentos'''

    def __init__(self, path):
        SnippetManagerBase.__init__(self)
        
        self._BD = Database(path)
        # se vuelven a reobtener los snippets desde esta nueva bd        
        self._Snippets = self.getAllSnippets()
        
        # trae si existe, el valor de la bd a cargar por defecto
        defaultBdName = self._Configs.defaultBdName
        if defaultBdName :          
            # obtiene el indice de la ruta de la bd a cargarce 
            pathBD = self.getPathBD(
                                self.getIndexBdName(defaultBdName))
            # crea la instancia de el catalogo en cuestion 
            self._BD = Database(pathBD)
            
            # instancia creada correctamente
            self._estado = True
            
        elif self._AllPathDBs:
            # sino, se carga la primer bd encontrada en la lista de bds
            self._BD = Database(
                        self.getPathDB(0))
        
            # diccionario con todas las instancia de objeto Snippet
            self.Snippets = self.getAllSnippets()
            # instancia creada correctamente
            self._estado = True

##########################
## Metodos de instancia ##
##########################

    def agregarSnippet(self, datosSnippet):
        ''' Recibe un dicionario de los datos de lo que sera un nuevo
        snippet y lo agrega a la BD.'''
        
        # llama al metodo de bd para agregar un snippet, devolviendo
        # el resultado de la operacion como boolean y en caso de error, 
        # el mensaje del error.
        resultado, mensaje = self._BD.agregarSnippet(datosSnippet)
        if resultado:
            # crea una instancia del nuevo snippet
            newSnippet = Snippet(datosSnippet)
            # agrega el nuevo snippet a los ya existentes
            self._addNewSnippetToCollection(newSnippet)
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
        if self._BD.eliminarSnippet(
            unSnippet.titulo, unSnippet.lenguaje):
                # quita del diccionario el snippet
                self.Snippets.pop((unSnippet.lenguaje,
                                        unSnippet.titulo))
                # establece como actual snippet a None
                self._SnippetActual = None
                return True
        else:
            return False

    def modificarSnippet(self, clave_spviejo, snippet_nuevo):
        ''' Actualiza el snippet cargado en memoria'''
        snippet =  self._Snippets[clave_spviejo].__dict__
        
        del self._Snippets[clave_spviejo]
        self._Snippets[
                (snippet_nuevo['language'],snippet_nuevo['title'])
                    ] = Snippet(snippet_nuevo)
    
        snippet_viejo = {}
        for campo in snippet :
            snippet_viejo[ campo.split('__')[1] ] = snippet[campo]
        return self._BD.modificarSnippet(snippet_viejo, snippet_nuevo)
        
    def newSnippet(self, tuplaSnippet):
        ''' Crea una instancia de snippet. '''
        
        # a partir de los valores que vienen en la tupla, 
        # se crea una instancia de snippet con dichos valores.
        nuevoSnippet = Snippet({
            'title':tuplaSnippet[0],
            'language':tuplaSnippet[1],
            'tags':tuplaSnippet[2],
            'contens':tuplaSnippet[3],
            'description':tuplaSnippet[4],
            'creation':tuplaSnippet[5],
            'reference':tuplaSnippet[6],
            'modified':tuplaSnippet[7],
            'uploader':tuplaSnippet[8],
            'starred':tuplaSnippet[9]})
            
        # tupla que sera de clave en el diccionario de los snippets
        clave = (tuplaSnippet[1],tuplaSnippet[0])
        
        elemento_diccionario = (clave,nuevoSnippet)

        return elemento_diccionario

#################
## Metodos Get ##
#################

    def getAllLenguajes(self):
        ''' Obtiene una lista de los lenguajes desde la bd.'''
        
        # obtiene desde la actual instancia de bd los lenguajes existentes 
        all_lenguajes = self._BD.getLenguajes()
        lenguajes = []
        # saca de la tupla y carga en la lista los lenguajes obtenidos
        #~ for lenguaje in all_lenguajes:
            #~ lenguajes.append(lenguaje[0])
        map(lambda lenguaje: lenguajes.append(lenguaje[0]), all_lenguajes)
        return lenguajes
        
    def getAllSnippets(self):
        ''' Obtiene los snippets desde la bd y carga en un diccionario
        los snippets en formato objeto Snippet().'''
        
        # obtiene desde la bd todos los snippets,
        # orden en que vienen los campos
        # 1-title,2-language,3-tags,4-contens,5-description
        # 6-creation,7-reference,8-modified,9-uploader,10-starred
        all_snippets = self._BD.getAllSnippets()
        
        # se aplica map para crear por cada tupla obtenida desde la bd
        # una tupla de tuplas donde el formato resultante es:
        # (claveSnippet : instanciaSnippet)
        todos_los_snippets = map(self.newSnippet,all_snippets)
        
        # dict(), convierte la tupla de tuplas a diccionario
        return dict(todos_los_snippets)

    def getLengsAndTitles(self,consulta=None, favorito = None):
        ''' Obtiene los snippets por lenguajes desde la bd.'''
        #~ tagsPresicion = bool(self._DBUtils.configs.searchPresitionTags)
        tagsPresicion = False
        return self._BD.getLengAndTitles(consulta, favorito, tagsPresicion)
    
#################
## Metodos Set ##
#################
