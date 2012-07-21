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

from gui import GUI
from pastebin import Pastebin
from couch_support.snippetmanager import SnippetManagerCouch
from snippetmanager import SnippetManager
from sm_base import SnippetManagerBase
from configurations import Configurations
from dbutils import DBUtils


class Fragmentos :
    ''' Clase que hace de puente entre la logica del programa con las interfaces graficas. '''
    
    def __init__(self) :
        self.BDU = DBUtils()
        self.ConfigsApp = Configurations()
        self.Pastebin = Pastebin()
        #self.SM = SnippetManager(self.BDU, self.ConfigsApp)
        self.SM = SnippetManagerBase()
        self.GUI = GUI(self)
        
    def getSM(self):
        pass
    
    def setSM(self, path, databasename = None):
        if not databasename :
            self.SM = SnippetManager(path)
        else:
            self.SM = SnippetManagerCouch(path, databasename)
        return self.SM
        
def main():
    Fragmentos()

if __name__ == '__main__':
    main()

