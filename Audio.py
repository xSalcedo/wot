import eyed3
import easygui
import os
import shutil

## función para cargar la canción

def load_audio(path):

	## se define una variable que carga la canción en la ruta, usando la librería eyed3
	
	load_song = eyed3.load(ruta)
	
	## variables para cada uno de los parámetros de los metadatos.
	
	artista = str(load_song.tag.artist)
	titulo = str(load_song.tag.title)
	disco = str(load_song.tag.album)
	fecha = str(load_song.tag.recording_date)
	genero = str(load_song.tag.genre)
		
	## os.path.basename devuelve el nombre del archivo a partir de la ruta completa.
		
	nombre = os.path.basename(ruta)
	print("Se ha cargado satisfactoriamente el archivo '" + nombre + "' en la librería.")
	
	## definición de la ruta donde se va a copiar el archivo que se cargó
	
	dest = base_path + "\\Library\\Audio\\"  + artista + " - " + titulo + ".mp3"
	
	## copia del archivo de la ubicación original a la librería
	
	shutil.copyfile(ruta, dest)
	
	## El código para leer las últimas líneas del archivo de librería
	
	lib_edit = open(base_path + "\\Library\\library.txt", "r")
	lineas = lib_edit.readlines()
	lib_edit.close()
	
	if len(lineas) == 0:
		last = "empty"
	else:	
		last = lineas[len(lineas) - 2]
	
	print("El ultimo registro es: " + last)
	
	## el método .write escribe en la última línea del archivo los datos de la canción cargada.
	
	with open(base_path + "\\Library\\library.txt", "a") as lib_edit:
		lib_edit.write(";" + artista + ";" + disco + ";" + fecha + ";" + titulo + ";" + genero + ";" + "audio\n")

base_path = "C:\Python\AlejoAmp"

######################
### Texto de menú  ###
######################

main_menu = "\nBienvenido al reproductor multimedia. Estas son las opciones disponibles:\n\n1. Cargar archivos\n2. Abrir la biblioteca\n3. Salir\n"
menu_1 = "\nCargar archivos\n\n1.1. Seleccionar archivo para cargar.\n1.2. Regresar al menú anterior\n"
menu_2 = ""

## Loop infinito del programa

while 1 == 1:
	temp = 0

######################
### Menú principal ###
######################

	print(main_menu)
	seleccion = input("Ingrese una opción: ")

	## Loop del menú de cargar canciones.

	if seleccion == "1":
		while temp == 0:
		
			print(menu_1)
			seleccion = input("Ingrese una opción: ")
				
			if seleccion =="1":
			
				## ruta es un string que almacena la ruta del archivo seleccionado con
				## el fileopenbox. después se llama a la funció load_audio pasándole como
				## parámetro la ruta del archivo.
			
				ruta = easygui.fileopenbox()
				load_audio(ruta)
				temp = 1
				
			elif seleccion =="2":
				break
			else:
				print("Por favor ingrese una opción válida: ")
		
	elif seleccion == "2":
		print(menu_2)
	elif seleccion == "3":
		print("\nGracias por usar el reproductor multimedia.")
		break
	else:
		print("Por favor ingrese una opción válida: ")
