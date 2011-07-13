#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
#       Copyright 2011 Emiliano Fernandez <emilianohfernandez@gmail.com>
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

import sqlite3
from busqueda import Busqueda

#~
class Database:

    def __init__(self,rutaBD):
        ''' Costructor de la clase. '''
        #~ print 'my path es: ',rutaBD
        self.__pathBD = rutaBD
        #conecta a la base de datos
        self.__connection = sqlite3.connect(self.__pathBD)
        #activa el cursor
        self.__cursor = self.__connection.cursor()
        #~ print 'Una instancia de BD fue creada con exito...',#rutaBD
        self.__Busqueda = Busqueda()

###############
# METODOS BD  #
###############

    def getPathBD(self):
        ''' Obtiene la ruta de la base de datos en uso. '''
        return self.__pathBD

    def getLenguajes(self):
        ''' Obtiene los lenguajes para la actual BD. '''
        resultado = self.realizarConsulta('SELECT DISTINCT language FROM snippet ORDER BY language')
        return resultado

    def getLengAndTitles(self,consulta=None):
        ''' Obtiene los snippets por lenguajes de la actual BD.'''
        if not consulta:
            resultado = self.realizarConsulta('SELECT language,title FROM snippet ORDER BY language,title')
        else:
            consulta = self.__Busqueda.generarConsulta(consulta)
            resultado = self.realizarConsulta(consulta)
        return resultado

    def getAllSnippets(self):
        ''' Obtiene todos los snippets de la base de datos. '''
        resultado = self.realizarConsulta('''SELECT title,language,tags,contens,
                                                    description,creation,reference,
                                                    modified,uploader,starred
                                            FROM snippet
                                            ORDER BY language,title''')
        return resultado

    def getSnippet(self, lenguaje, titulo):
        ''' Obtiene un snippet por su lenguaje y titulo correspondiente. '''
        resultado = self.realizarConsulta("SELECT * FROM snippet WHERE language = '"+lenguaje+"' AND title = '"+titulo + "'")
        return self.__convertirASnippet(resultado)

    def getSnippetsCount(self):
        ''' Obtiene la cantidad de snippets cargados en la actual bd. '''
        cantidad = self.realizarConsulta('SELECT count(*) FROM snippet')
        return int(cantidad[0][0])

    def realizarConsulta(self,consulta):
        ''' Realiza una consulta a la base de datos. '''
        #TODO:evitar los self
        #~ print consulta
        cursor_temp = self.__cursor.execute(consulta)
        lista = []
        for fila in cursor_temp:
            lista.append(fila)
        #~ print 'Consulta completa...'
        return lista

################################
# METODOS PARA MANEJAR SNIPPET #
################################

    def agregarSnippet(self, datosSnippet):
        ''' Agrega un nuevo Snippet a la base de datos. '''

        # TODO: agregar los try-catch para contemplar:
        # º snippet repetido
        # º error al agregar un snippet

        #genera los sig de preguntas segun la cantidad de campos recibidos
        sp = str('('+'?,'*len(datosSnippet))[:-1] + ')'
        #genera un string con los nombre de los campos
        campos = '('+','.join(datosSnippet.keys())+')'
        try:
            self.__cursor.execute('INSERT INTO snippet '+campos+' VALUES '+sp, datosSnippet.values())
            self.__connection.commit()
            return True, None
        #~ except sqlite3.OperationalException,msg:
        except Exception, msg:
            print 'agregarSnippet >> ',msg
            return False, str(msg)

    def eliminarSnippet(self,titulo,lenguaje):
        ''' Elimina un Snippet de la bd.'''

        sql = u'DELETE FROM snippet ' + \
        'WHERE title = "{0}" AND language = "{1}"'.format(titulo,lenguaje)
        print sql
        try:
            self.__cursor.execute(sql)
            self.__connection.commit()
            print "Un registro fue eliminado."
            return True
        except Exception, msg:
            print 'eliminarSnippet: ',msg
            return False

######################
# METODOS AUXILIARES #
######################


    def __convertirASnippet(self,datos):
        ''' Obtiene los datos de un snippet desde la BD, y los
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


