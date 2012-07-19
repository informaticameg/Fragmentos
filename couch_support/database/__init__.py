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

from busqueda import Busqueda
import couchdb

class Database:
    ''' Clase manejadora de operaciones con una base de datos/catalogo. '''
    
    def __init__(self,rutaBD, database_name):
        u''' Costructor de la clase. '''
        self.__pathBD = rutaBD
        self.__Busqueda = Busqueda()
        self.bd = couchdb.Server(rutaBD)[database_name]
        
###############
# METODOS BD  #
###############

    def getPathBD(self):
        u''' Obtiene la ruta de la base de datos en uso. '''
        return self.__pathBD

    def getLenguajes(self):
        u''' Obtiene los lenguajes para la actual BD. '''
        resultado = self.bd.query("""
            function (doc) {
                if (doc.doc_type == 'snippet') {
                    emit(doc.language, null);
        };}""")
        return list(tuple([doc['key'] for doc in resultado]))

    def getLengAndTitles(self, consulta=None, favorito = None, tagsPresicion = None):
        u''' Obtiene los snippets por lenguajes de la actual BD.
            
            @return: lista de tuplas con este formato: (lenguaje,titulo)'''
        #por defecto busca los que no son favoritoss
        if not consulta and not favorito:
            resultado = self.bd.query('''
                function (doc) {
                    if (doc.doc_type == 'snippet') {
                        emit([doc.language, doc.title]);
                };}''')
            return [doc['key'] for doc in resultado]
        else:
            #si no se pasa este parametro
            if favorito is None: 
                favorito = 0
            if tagsPresicion is None:
                tagsPresicion = False
            #genera un sql con la busqueda segun la consulta recibida
            consulta = self.__Busqueda.generarConsulta(consulta, int(favorito), tagsPresicion)
            #obtiene los resultados de la consulta
            resultado = self.bd.query(consulta)
            return [(doc['key'],doc['value']) for doc in resultado]

    def getAllSnippets(self):
        u''' Obtiene todos los snippets de la base de datos. '''
        orden = ['title','language','tags','code','description','creation','modified','uploader','starred','reference']
        resultado = self.bd.query("""
            function (doc) {
                if (doc.doc_type == 'snippet') {
                    emit(doc.title, doc);
        };}""")
        self.cant_snippets = len(resultado)
        return [doc['value'] for doc in resultado]

    def getSnippet(self, lenguaje, titulo):
        u''' Obtiene un snippet por su lenguaje y titulo correspondiente. '''
        resultado = self.bd.getDatosColumnas("snippet",criterios = {'language':lenguaje,'title':titulo})
        return self.__convertirASnippet(resultado)

    def getSnippetsCount(self):
        u''' Obtiene la cantidad de snippets cargados en la actual bd. '''
        resultado = self.bd.query('''
            function (doc) {
               if (doc.doc_type == 'snippet') {
                 emit(null, doc.title);
            };}''')
        return len([doc for doc in resultado])

    def realizarConsulta(self,consulta):
        return []

################################
# METODOS PARA MANEJAR SNIPPET #
################################

    def agregarSnippet(self, datosSnippet):
        u''' Agrega un nuevo Snippet a la base de datos. 
        datosSnippet = diccionario con los datos del snippet a agregar.'''
#        try:
        print self.bd.__dict__
        self.bd.save(datosSnippet)
        return True, ''
#        except Exception, msg:
#            return False, str(msg)
        

    def eliminarSnippet(self,titulo,lenguaje):
        u''' Elimina un Snippet de la bd.'''
        try:
            resultado = self.bd.query("""
                function (doc) {
                   if (doc.title == "%s" && doc.language == "%s") {
                      emit(null, doc);
                };}""" % (titulo,lenguaje))
            self.bd.delete([doc['value'] for doc in resultado][0])
            return True
        except Exception, msg:
            print 'eliminarSnippet: ',msg
            return False
        
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


