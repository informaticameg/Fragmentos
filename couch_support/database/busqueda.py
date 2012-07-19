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

class Busqueda :
    '''(NULL)'''

    def __init__(self):
        self.diccampos = {
        't=' : 'title',
        'l=':'language',
        'g=':'tags',
        'c=':'contens',
        'd=':'description',
        'r=':'reference',
        'n=':'creation',
        'm=':'modified',
        'u=':'uploader',
        }
        
    def generarConsulta (self, labusqueda, enfavoritos, tagsPresicion) :
        """ recibe la busqueda completa y genera un sql para realizar la busqueda """
        listadecriteriosseparados = self.__separarPorCampos(labusqueda)
        if listadecriteriosseparados:
            query = self.__generarView(listadecriteriosseparados, enfavoritos, tagsPresicion)
        else :
            query = """function (doc) {
                   if (doc) {
                      emit(doc.language, doc.title);
                };}"""
        return query

    def __separarPorCampos (self, labusqueda) :
        """ separa la busqueda en una lista donde cada elemento es el criterio a buscar por campo """
        #CAUTION!!! Magic. Do not touch
        #~ labusqueda = 'f=sadsdas,t=dadfd and gernedsa,g=dsfbusdfud'
        listadecriterios = []
        if labusqueda.find('=') == -1:
            #caso en que solo escribas titulo(o sea nada)
            listadecriterios.append('t='+labusqueda)
        else:
            if labusqueda.find(',') == -1:
                #caso en que escribas un solo campo para buscar ej: t=hola
                if len(labusqueda) > 2 :
                    listadecriterios.append(labusqueda)
                else:
                    listadecriterios = False
            else:
            #caso en que tengas todo ej: t=hola,l=python
                listadecriterios = labusqueda.split(',')
                if len(listadecriterios[-1]) < 3 :
                    listadecriterios = False

        return listadecriterios

    def __generarConsultaSimple (self, campo, tagsPresicion) :
        """ devuelve el criterio del campo simple buscado """
        #esto es para __generarSQL

        #~ campo = 'g=agua'
        if campo[:2] == 'g=':#%,atr,%-%,atr-atr,%-atr
            if tagsPresicion :
                query = """(doc.tags.indexOf('%s') != -1)""" % campo[2:]
            else:
                query = """(doc.tags.indexOf('%s') != -1)""" % campo[2:]
                
        elif campo[:2] in ['l=','t=','c=','d=','r=','u=']:#atr%
            query = '(doc.%s.toLowerCase().indexOf("%s") != -1) ' % (self.diccampos[campo[:2]],campo[2:]) 
        elif campo[:2] in ['n=','m=']:#atr%
            query = '(doc.%s.indexOf("%s") != -1) ' % (self.diccampos[campo[:2]],campo[2:])
        else:#no deberia pasar
            print 'error: '
            query = False

        return query

    def __generarConsultaCompleja (self, campocomplejo, tagsPresicion) :
        """ Devuelve la query del campo complejo buscado """
        #solo soportado para operadores del mismo tipo,
        #ej: aaa and bbb; cc or ddd or fff

        operador_js = {' and ':' && ' ,' or ':' || '}
        operador = ' and ' if campocomplejo.find(' and ') != -1 else ' or '
        
        criterios = campocomplejo[2:].split(operador)
        query = '('
        for criterio in criterios:
            query += self.__generarConsultaSimple(campocomplejo[:2]+criterio, tagsPresicion) + operador_js[operador]
        return query[:-3] + ')'

    def __generarView (self, listadecampos, favorito, tagsPresicion) :
        """ recibe una lista de campos y genera la view para realizar la busqueda 
        Si favorito = 1, busca en los favoritos."""
        consulta = ''
        js_consulta = """function (doc) {
                   if (%s) {
                      emit(doc.language, doc.title);
                };}"""
        for campo in listadecampos:
            if (campo.find(' and ') == -1) and (campo.find(' or ') == -1):
                consulta += self.__generarConsultaSimple(campo, tagsPresicion)
            else:
                consulta += self.__generarConsultaCompleja(campo, tagsPresicion)
            consulta += " && "
        if favorito == 1:
            consulta += "(doc.starred == 1) && " 
        return js_consulta % consulta[:-4]

if __name__ == '__main__':
    b = Busqueda()
    print b.generarConsulta('g=archivo,l=pascal', 0)
