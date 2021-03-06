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

from PyQt4 import QtGui
#el import a lo bruto se salva por la cantidad de lexers
from PyQt4.Qsci import * #@UnusedWildImport


class Scintilla:
    
    def __init__(self):

        editor = QsciScintilla()
        editor.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)

        ## define the font to use
        font = QtGui.QFont()
        #font.setStyleHint (QtGui.QFont.Monospace,strategy=QtGui.QFont.PreferDefault)
        #~ font.setFamily("Default")
        #font.setFixedPitch(True)
        #font.setPointSize(10)
        # the font metrics here will help
        # building the margin width later
        fm = QtGui.QFontMetrics(font)

        ## set the default font of the editor
        ## and take the same font for line numbers
        editor.setFont(font)
        editor.setMarginsFont(font)

        ## Line numbers
        # conventionnaly, margin 0 is for line numbers
        editor.setMarginWidth(0, fm.width( "00000" ))
        editor.setMarginLineNumbers(0, True)

        ## Edge Mode shows a red vetical bar at 80 chars
        #~ editor.setEdgeMode(QsciScintilla.EdgeLine)
        #~ editor.setEdgeColumn(80)
        #~ editor.setEdgeColor(QtGui.QColor("#FF0000"))

        ## Folding visual : we will use boxes
        editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        ## Braces matching
        editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        ## Editing line color
        editor.setCaretLineVisible(True)
        editor.setCaretLineBackgroundColor(QtGui.QColor("#F5F5DC"))

        ## Margins colors
        # line numbers margin
        editor.setMarginsBackgroundColor(QtGui.QColor("#E5E5E5"))
        editor.setMarginsForegroundColor(QtGui.QColor("#1A1A1A"))

        # folding margin colors (foreground,background)
        #~ editor.setFoldMarginColors(QtGui.QColor("#99CC66"),QtGui.QColor("#333300"))
        editor.setFoldMarginColors(QtGui.QColor("#FFFFFF"),QtGui.QColor("#E5E5E5"))
        

        self.__editor = editor
        self.__font = font
        
        #
        self.__equivalentes = {
            'C++':'CPP',
            'Css':'CSS',
            'C':'CPP',
            'C#':'CSharp',
            'Html':'HTML',
            'MsSql':'SQL',
            'Sql':'SQL',
            'Xml':'XML',
            'CoffeScript':'Python',
            'VB':'Custom',
            'VB6':'Custom',
        }
        
    def getLanguages(self):
        ''' '''
        #TODO: devolver junto con los sci lenguajes, los reemplazos
        import PyQt4.Qsci
        langs = [i for i in dir(PyQt4.Qsci) if i.startswith('QsciLexer')]
        langs = langs[1:]
        langs = [lang[9:] for lang in langs]
        langs += self.__equivalentes.keys()
        langs.sort()
        for leng in ['CPP','CSharp'] :
            langs.remove(leng)
        return langs

    def getCode(self):
        ''' Devulve el codigo convertido en utf-8/unicode. '''
        return unicode(self.__editor.text().toUtf8(),'utf-8')
        
    def getEditor(self):
        ''' '''
        return self.__editor
    
    def setLanguage(self,lenguaje):
        ''' Establece el coloreo de sintaxis correspondiente. '''
        
        if lenguaje in self.__equivalentes:
            lenguaje = self.__equivalentes[lenguaje]
            
        import PyQt4.Qsci
        langs = [i for i in dir(PyQt4.Qsci) if i.startswith('QsciLexer')]

        if 'QsciLexer'+lenguaje in langs:
            ## Choose a lexer
            #print globals()
            lexer = globals()['QsciLexer'+lenguaje]()#cargador magico de clases
            #~ lexer.setDefaultFont(self.__font)
            self.__editor.setLexer(lexer)
            ## Render on screen
            self.__editor.show()
            ## Show this file in the editor
            #~ self.__editor.setText(codigo)
        else:
            print 'QsciLexer'+lenguaje+ ' no fue encontrado'
            #~ print langs
            
    def setCode(self,codigo):
        ''' '''
        ## Show this file in the editor
        self.__editor.setText(codigo)

    def setFullCode(self,codigo,lenguaje):
        ''' '''
        self.setCode(codigo)
        self.setLanguage(lenguaje)

    def setFocus(self):
        """ Put focus in editor. """
        self.__editor.setFocus()

    def copyToClipboard(self):
        pass

    def clearCode(self):
        self.__editor.setText("")
        
