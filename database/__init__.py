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

import sqlite
from busqueda import Busqueda


class Database:
    ''' Clase manejadora de operaciones con una base de datos/catalogo. '''
    
    def __init__(self,rutaBD):
        u''' Costructor de la clase. '''
        self.__pathBD = rutaBD
        self.__Busqueda = Busqueda()
        
        self.bd = sqlite.sqlite(self.__pathBD)

###############
# METODOS BD  #
###############

    def getPathBD(self):
        u''' Obtiene la ruta de la base de datos en uso. '''
        return self.__pathBD

    def getLenguajes(self):
        u''' Obtiene los lenguajes para la actual BD. '''
        resultado = self.bd.realizarConsulta('SELECT DISTINCT language FROM snippet ORDER BY language')
        return resultado

    def getLengAndTitles(self, consulta=None, favorito = None, tagsPresicion = None):
        u''' Obtiene los snippets por lenguajes de la actual BD.
        
            @return: una lista de tuplas con este formato (lenguaje,titulo)'''
        
        #por defecto busca los que no son favoritos
        if not consulta and not favorito:
            resultado = self.bd.realizarConsulta('''SELECT language,title 
                                                FROM snippet  
                                                ORDER BY language,title ''')
        else:
            #si no se pasa este parametro
            if favorito is None: 
                favorito = 0
            if tagsPresicion is None:
                tagsPresicion = False
            #genera un sql con la busqueda segun la consulta recibida
            consulta = self.__Busqueda.generarConsulta(consulta, int(favorito), tagsPresicion)
            #obtiene los resultados de la consulta
            resultado = self.realizarConsulta(consulta)
        return resultado

    def getAllSnippets(self):
        u''' Obtiene todos los snippets de la base de datos. '''
        resultado = self.bd.realizarConsulta('''SELECT title,language,tags,contens,
                                                    description,creation,reference,
                                                    modified,uploader,starred
                                            FROM snippet
                                            ORDER BY language,title''')
        return resultado

    def getSnippet(self, lenguaje, titulo):
        u''' Obtiene un snippet por su lenguaje y titulo correspondiente. '''
        resultado = self.bd.getDatosColumnas("snippet",criterios = {'language':lenguaje,'title':titulo})
        return self.__convertirASnippet(resultado)

    def getSnippetsCount(self):
        u''' Obtiene la cantidad de snippets cargados en la actual bd. '''
        cantidad = self.realizarConsulta('SELECT count(*) FROM snippet')
        return int(cantidad[0][0])

    def realizarConsulta(self,consulta):
        return self.bd.realizarConsulta(consulta)

################################
# METODOS PARA MANEJAR SNIPPET #
################################

    def agregarSnippet(self, datosSnippet):
        u''' Agrega un nuevo Snippet a la base de datos. 
        datosSnippet = diccionario con los datos del snippet a agregar.'''

        # TODO: agregar los try-catch para contemplar:
        # º snippet repetido
        # º error al agregar un snippet

        #genera los sig de preguntas segun la cantidad de campos recibidos
        sp = str('('+'?,'*len(datosSnippet))[:-1] + ')'
        #genera un string con los nombre de los campos
        campos = '('+','.join(datosSnippet.keys())+')'
        #se convierten los campos a unicode/utf8
        valores = []
        for valor in datosSnippet.values():
            valores.append(valor)#.encode('ascii','utf-8'))        
        try:
            return self.bd.realizarAlta("snippet", datosSnippet) , None
        except Exception, msg:
            print 'agregarSnippet >> ',str(msg)
            return False, str(msg)

    def eliminarSnippet(self,titulo,lenguaje):
        u''' Elimina un Snippet de la bd.'''

        condiciones = ['title = "%s"' % titulo, 'language = "%s"' % lenguaje]
        try:
            return self.bd.realizarBaja("snippet", condiciones)
        except Exception, msg:
            print 'eliminarSnippet: ',msg
            return False

    def modificarSnippet(self, snippet_viejo, snippet_nuevo):
        consulta = """UPDATE snippet 
            SET title = ?,
                language = ?,
                tags = ?,
                contens = ?,
                description = ?,
                reference = ?,
                modified = ?,
                uploader = ?,
                starred = ?
            WHERE title = ? 
            AND language = ?""" 
        return self.bd.realizarNoConsulta(consulta, 
                (
                 snippet_nuevo['title'],
                 snippet_nuevo['language'],
                 snippet_nuevo['tags'],
                 snippet_nuevo['contens'],
                 snippet_nuevo['description'],
                 snippet_nuevo['reference'],
                 snippet_nuevo['modified'],
                 snippet_nuevo['uploader'],
                 snippet_nuevo['starred'],
                 
                 snippet_viejo['titulo'],
                 snippet_viejo['lenguaje']
                 ))
        
######################
# METODOS AUXILIARES #
######################


    def __convertirASnippet(self,datos):
        u''' Obtiene los datos de un snippet desde la BD, y los
        carga en un diccionario, para luego convertirse en una
        instancia de Snippet. '''

        snippet = {
        'title':datos[0][0],
        'language':datos[0][1],
        'contens':datos[0][2],
        'tags':datos[0][3],
        'description':datos[0][4],
        'creation':datos[0][5],
        'starred':datos[0][6],
        'reference':datos[0][7],
        'modified':datos[0][8],
        'uploader':datos[0][9]
        }
        return snippet


