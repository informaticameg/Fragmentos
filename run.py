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

from fragmentos import Fragmentos


class Main :
    u''' Clase que hace correr la aplicación.'''

    def __init__(self) :
        self.validar()
        self.Fragmentos = Fragmentos()

    def validar (self) :
        from validar import Validator,ValidarShorcuts
        v = Validator()
        # ejecuta los metodos para chequear el estado
        # de la aplicacion
        v.check()
        import os
        if os.name == 'posix':
            ValidarShorcuts()

def main():
    import os
    if os.name == 'posix':
        import fcntl
        pid_file = 'Singleton'
        fp = open(pid_file, 'w')
        try:
            fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            Main()
            exit(0)

        except IOError:
            # another instance is running
            print 'Ya hay otra instancia corriendo'
            exit(0)
    elif os.name == 'nt':
        Main()
        exit(0)

if __name__ == '__main__':
    main()

