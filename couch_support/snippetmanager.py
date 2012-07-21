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

from snippet import Snippet
from sm_base import SnippetManagerBase
from couch_support.database import Database


class SnippetManagerCouch (SnippetManagerBase):
    ''' Clase que hace de wrapper entre las clases
    de la logica del programa, con la clase Fragmentos'''

    def __init__(self, path, db_name):
        SnippetManagerBase.__init__(self)
        self.loadAllPathDBs()
        
        self._BD = Database(path, db_name)
        # se vuelven a reobtener los snippets desde esta nueva bd        
        self._Snippets = self.getAllSnippets()

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
                self._Snippets.pop((unSnippet.lenguaje,
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
            'starred':spt['starred']}
             )
            
        # tupla que sera de clave en el diccionario de los snippets
        clave = (spt['language'],spt['title'])
        return (clave,nuevoSnippet)

#################
## Metodos Get ##
#################

    def getAllLenguajes(self):
        ''' Obtiene una lista de los lenguajes desde la bd.'''
        
        # obtiene desde la actual instancia de bd los lenguajes existentes 
        lenguajes = self._BD.getLenguajes()
        lenguajes.sort()
        return lenguajes
    
    def getAllSnippets(self):
        ''' Obtiene los snippets desde la bd y carga en un diccionario
        los snippets en formato objeto Snippet().'''
        
        all = self._BD.getAllSnippets()
        return dict([self.newSnippet(snippet) for snippet in all])

    def getLengsAndTitles(self,consulta=None, favorito = None):
        ''' Obtiene los snippets por lenguajes desde la bd.'''
        #~ tagsPresicion = bool(self.__DBUtils.configs.searchPresitionTags)
        tagsPresicion = False
        return self._BD.getLengAndTitles(consulta, favorito, tagsPresicion)

    def getSnippetsCount(self):
        ''' Devuelve un entero con la cantidad de snippets cargados en la BD.'''
        return self._BD.getSnippetsCount()

    def getPathDB(self, index):
        ''' Recupera de la lista de bds la ruta en el indice especificado.'''
        return self._AllPathDBs[index]

#################
## Metodos Set ##
#################

#if __name__ == '__main__':
#    s = SnippetManager()
#    s.setDB('http://192.168.1.5:5984/','sourcecode')
#    
