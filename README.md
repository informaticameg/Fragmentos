# Fragmentos

> Simple snippet manager

<img src="https://raw.github.com/informaticameg/Fragmentos/master/fragmentos.png" />

## That is fragments?

Is a cataloguer and organizer of source code, which allows store your snippets to access them when needed.

Their slogan is: "write it once, find it forever."
     
## Amazing search system

You can search by title, tags, language, contens, description, date and author. 

Some examples:

- Search all python language snippets with tag date and time:

	`l=python,g=date and time`

- Search all snippets that contain the word import

	`c=import`

- Search all snippets of language C with the title 'string' and the tags trim or split

	`l=c,t=string,g=trim or split`

**List of possible search criteria:**
- t= title
- l=language
- g= tags
- c= contens
- d= description
- n= creation date
- m= modified date
- u= author/uploader
- s= starred. Value 1 for true.

## Technical

- Python 2.7
- PyQt 4.7
- SQLite

## How to run
	
	# install dependencies with this script
	$ sh install_dependencies.sh 

	# or manually
	$ apt-get install python-qt4 python-qscintilla2 python-qt4-dbus

	# and run it
    $ python run.py
        
## Licence

Copyright 2012 Informática MEG

Released under the GPL License.
