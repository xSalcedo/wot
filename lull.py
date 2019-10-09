import audio_metadata

"""Audio-metadata nos ayuda a extraer la metada de archivos .mp3
(requiere instalacion comando:'pip install audio-metadata')"""

import mutagen

"""mutagen nos ayuda a extraer la metada de archivos .mp4
(requiere instalacion comando:'pip install mutagen')"""

import os

"""os nos ayuda con el manejo de archivos en carpeta
(no requiere instalacion, pertenece a la libreria estandar)"""

import pickle

"""Pickle es una libreria que guarda objetos de python en archivos binarios
    con terminacion .pickle """

from exif import Image

"""Exif nos ayuda a extraer la metada de archivos .jpg y .png
(requiere instalacion comando:'pip install exif')"""


# -----------------------------------------------FUNCIONES PICKLE------------------------------------------
def createPickles(type_file):
    """Crea el archivo .pickle correspondiente al tipo de archivo (audio, video,
        musica y playlist), alli guardamos la informacion """
    #
    pickle_files = {'photo': 'fotos.pickle', 'music': 'musica.pickle', 'video': 'videos.pickle',
                    'album_music': 'album_music.pickle', 'album_photo': 'album_photo.pickle',
                    'album_video': 'album_video.pickle'}

    pickle_t = open(pickle_files[type_file], 'wb')
    pickle.dump([], pickle_t)  # Se crea el pickle guardando una lista vacia
    pickle_t.close()


def saveTags(tags, type_file):
    """Guarda los tags(artista, titulo etc.) retornados de cada funcion 'read'
        en el archivo pickle correspondiente """

    pickle_files = {'photo': 'fotos.pickle', 'music': 'musica.pickle', 'video': 'videos.pickle',
                    'album_music': 'album_music.pickle', 'album_photo': 'album_photo.pickle',
                    'album_video': 'album_video.pickle'}

    with open(pickle_files[type_file], 'rb') as pickle_file:
        all_tags = pickle.load(pickle_file)  # Abre el pickle en lectura binaria para extraer la lista guardada
        pickle_file.close()

    with open(pickle_files[type_file], 'wb') as pickle_file:
        all_tags.append(tags)  # Añade el nuevo tag a la lista
        pickle.dump(all_tags, pickle_file)  # Abre el pickle en escritura binaria para volver a guardar
        pickle_file.close()


def readTags(type_file):
    """Recibe el tipo de archivo y devuelve los datos guardados en el pickle"""

    pickle_files = {'photo': 'fotos.pickle', 'music': 'musica.pickle', 'video': 'videos.pickle',
                    'album_music': 'album_music.pickle', 'album_photo': 'album_photo.pickle',
                    'album_video': 'album_video.pickle'}

    with open(pickle_files[type_file], 'rb') as pickle_file:
        all_tags = pickle.load(pickle_file)  # Lee el archivo pickle
        pickle_file.close()

    return all_tags


def saveAllTags(all_tags_list, type_file):
    """Guarda el objeto recibido como primer argumento en el pickle de su tipo"""

    pickle_files = {'photo': 'fotos.pickle', 'music': 'musica.pickle', 'video': 'videos.pickle',
                    'album_music': 'album_music.pickle', 'album_photo': 'album_photo.pickle',
                    'album_video': 'album_video.pickle'}

    with open(pickle_files[type_file], 'wb') as pickle_file:
        pickle.dump(all_tags_list, pickle_file)  # Escribe en el pickle el primer argumento
        pickle_file.close()


def deleteTags(file_path, type_file):
    """Borra los datos de un archivo desde su ruta guardada, pide el tipo de archivo(music, video, photo) """

    all_tags = readTags(type_file)

    for dicc in all_tags:
        if dicc["file_name"] == file_path:  # Busca el archivo por su ruta
            all_tags.remove(dicc)

    saveAllTags(all_tags, type_file)


def destroy_info(type_file):
    pickle_files = {'photo': 'fotos.pickle', 'music': 'musica.pickle', 'video': 'videos.pickle',
                    'album_music': 'album_music.pickle', 'album_photo': 'album_photo.pickle',
                    'album_video': 'album_video.pickle'}

    os.remove(pickle_files[type_file])
    print("se ha borrado el archivo")
    createPickles(type_file)


# --------------------------------------------------FUNCIONES READ----------------------------------------------------------------
def modify(tags):
    """Pregunta al usuario si desea cambiar algun parametro, de ser asi, lo modifica"""

    print("los datos de su archivo son: " + str(tags))

    question = input("""Desea modificar algun parametro ?
                /////////////////////////
                - s ---- Si
                - n ---- No
                /////////////////////////
        """)
    if question == "s":
        # se crea la variable bucle, la cual tiene como proposito mantener el bucle del menú mientras se requiera
        bucle = 1
        while bucle == 1:
            print("""Estos son los datos que puede modificar:
                        /////////////////////////
                        - a ---- Album
                        - ar ---- Artist
                        - d ---- Date
                        - t ---- Title
                        - g ---- Genere
                        /////////////////////////
            """)
            bucl = 1
            while bucl == 1:
                select_tag = input()  # Se establece la lista de opciones que tiene el ususario.

                if select_tag == "a":
                    mod_tag = "album"
                    bucl = 0

                elif select_tag == "ar":
                    mod_tag = "artist"
                    bucl = 0

                elif select_tag == "d":
                    mod_tag = "date"
                    bucl = 0

                elif select_tag == "t":
                    mod_tag = "title"
                    bucl = 0

                elif select_tag == "g":
                    mod_tag = "genre"
                    bucl = 0

                else:
                    print("Opcion invalida, escriba denuevo")

            new_value = input("escriba el nuevo valor del dato: ")

            tags[mod_tag] = [new_value]
            print("sus nuevos valores son: " + str(tags))
            # Se crea la variable flag, la cual tiene como proposito guardar la información del usuario
            flag = input("""Desea modificar otro parametro ?
                        /////////////////////////
                        - s ---- Si
                        - n ---- No
                        /////////////////////////
			""")
			bucl2 = 1
			while bucl2 == 1:
				if flag == "n":
					bucle = 2
					bucl2 = 0
				elif flag == "s":
					bucl2 = 0
				else:
					print("Opción invalida")

    return tags


def readMusic(file_path):
    """Guarda en un diccionario toda la informacion del archivo,
    lo agrega al archivo pickle de musica  """

    for file in readTags("music"):
        if file["file_name"] == file_path:  # Se determina si el archivo ya es existente
            return None
    #
    tags = {"file_name": file_path, "album": ["Unknown"], "artist": ["Unknown"], "date": ["Unknown"],
            "title": [file_path], "genre": ["Unknown"]}  # Diccionario con la informacion a guardar

    song_data = audio_metadata.load(file_path)  # Carga metadata de la musica con la funcion audio_metadata.load

    keys = [x for x in song_data.tags]
    values = [x for x in song_data.tags.values()]
    meta_data = dict(zip(keys, values))  # Lo convierte en diccionario para facilitar su manejo

    for x in tags.keys():
        if x in meta_data:
            tags[x] = meta_data[x]  # Guarda solo la metadata que nos interesa

    saveTags(modify(tags), 'music')

    allSongs = readTags('music')
    print("Se añadio recientemente: ")
    print("--------------------------------------------")
    print("--------------------------------------------")
    for x in allSongs[2:0:-1]:  # Se muestra la musica añadida recientemente
        print("Name: ", x["title"], sep="  ")
        print("Data:")
        print(x["artist"], x["album"], x["date"], sep="\n")
        print("--------------------------------------------")
        print("--------------------------------------------")


def readPhoto(file_path):
    """Guarda en un diccionario toda la informacion del archivo,
    lo agrega al archivo pickle de fotos  """

    for file in readTags("photo"):
        if file["file_name"] == file_path:  # Se determina si el archivo ya es existente
            return None

    tags = {"file_name": file_path, "album": ["Unknown"], "artist": ["Unknown"], "date": ["Unknown"],
            "title": [file_path], "genre": ["Unknown"]}  # Diccionario con la informacion a guardar

    with open(file_path, 'rb') as image_file:
        my_image = Image(image_file)
    try:
        artist = my_image.make
    except:
        artist = "Unknown"
    try:
        date = my_image.datetime
    except:
        date = "Unknown"
    try:
        genere = my_image.scene_capture_type
    except:
        genere = "Unknown"

    tags = {"file_name": file_path, "album": ["Unknown"], "artist": [artist], "date": [date],
            "title": [file_path], "genre": [genere]}

    saveTags(modify(tags), 'photo')

    allPhotos = readTags('photo')
    print("Se añadio recientemente: ")
    print("--------------------------------------------")
    print("--------------------------------------------")
    for x in allPhotos[2:0:-1]:  # Se muestran las fotos añadidas recientemente
        print("Name: ", x["title"], sep="  ")
        print("Data:")
        print(x["artist"], x["album"], x["date"], sep="\n")
        print("--------------------------------------------")
        print("--------------------------------------------")


def readVideo(file_path):
    """guarda en un diccionario toda la informacion del archivo,
    lo agrega al archivo pickle de video  """

    for file in readTags("video"):
        if file["file_name"] == file_path:  # Se determina si el archivo ya es existente
            return None

    tags = {"file_name": file_path, "album": ["Unknown"], "artist": ["Unknown"], "date": ["Unknown"],
            "title": [file_path], "genre": ["Unknown"]}  # Diccionario con la informacion a guardar
    info = mutagen.File(file_path,
                        easy=True)  # guarda los datos de la metadata del video mediante funciones en la libreria mutagen
    for key in tags:  # recorre las keys de los datos del video
        if key not in info.keys():  # compara las keys de los datos del video con las keys que necesitamos en tags
            pass
        else:  # si hay alguna key que que está en tags y está en los datos del video
            tags[key] = info[key]  # le asignamos el valor de la key de los datos a el valor de la key en los tags
    saveTags(modify(tags), 'video')
    allVideos = readTags('video')
    print("Se añadio recientemente: ")
    print("--------------------------------------------")
    print("--------------------------------------------")
    for x in allVideos[2:0:-1]:  # Se muestran los videos añadidos recientemente
        print("Name: ", x["title"], sep="  ")
        print("Data:")
        print(x["artist"], x["album"], x["date"], sep="\n")
        print("--------------------------------------------")
        print("--------------------------------------------")


# --------------------------------------------------------FUNCIONES ESPECIFICAS----------------------------------------------------------------

def filterBy(tag, seccion, specified="todo"):
    """ funcion que filtra una seccion(musica,video,foto) de acuerdo
        a un tag(artist,album,date) y muestra en pantalla el
        el resultado del filtro"""

    dates = list(readTags(seccion))  # variable que almacena los datos que hay de música

    final_filter = []  # variable para almacenar los datos a imprimir

    filter_tag = []  # variable para almacenar los opciones  del tipo de tag escogido

    if tag == "title":  # si el tag ingresado es "title" unicamente va a imprimir los nombres de las canciones
        for info_file in dates:  # recorre dates obteniendo el diccionario de cada archivo
            final_filter.append(info_file["title"][0].lower())  # agrega a final_filter el titulo de cada archivo
        final_filter.sort()  # organiza los datos alfabeticamente

        for name_title in final_filter:
            """imprime los datos que fueron requeridos por el usuario"""
            print("     --", name_title)
            print("\n")
    else:  # si el tag es diferente de "title" el programa ejecuta lo siguiente
        for info_file in dates:  # recorre dates y obtiene cada diccionario de cada archivo
            value_tag_in_info_file = info_file[tag][
                0].lower()  # almacena el valor del tag correspondiente a cada archivo
            if value_tag_in_info_file not in filter_tag:
                filter_tag.append(value_tag_in_info_file)  # si el valor no está repetido, lo agrega a filter_tag

        filter_tag.sort()  # organiza final_tag

        for option in filter_tag:
            final_filter.append([option])  # agrega cada elemento de filter tag como una lista a la lista final_filter

        for index in range(len(final_filter)):
            """recorre cada diccionario de cada archivo comparando el valor del tag
             respectivo con cada uno de los elementos de final_filter para obtener
             los archivos que tienen el mismo valor del tag y los agreaga a la lista
             de listas correspondiente"""

            for info_file in dates:  # recorre dates y obtiene cada deiccionario de cada archivo de la seccion
                value_tag_in_info_file = info_file[tag][
                    0].lower()  # almacena el valor del tag requerido de cada archivo

                if value_tag_in_info_file == final_filter[index][
                    0]:  # compara si el valor del tag requerido está en cierto indice de la lista final_filter
                    final_filter[index].append(
                        info_file["title"][0])  # si es así, agrega el nombre del archivo comparado a final_filter.

        if specified == "todo":
            """imprime todos los datos, organizados por el tag ingresado"""
            for option_tag in final_filter:  # recorre final_filter obteniendo cada lista de opciones de tag con sus elementos
                print(tag, option_tag[0], ":")  # imprime tag
                for n in range(1, len(option_tag)):  # recorre los elementos de cada lista de opciones de tag
                    print("     --",
                          option_tag[n])  # imprime los elementos de la lista recorrida desde el indice 1 al ultimo
                print("\n")  # los elementos impresos corresponden a los titulos de los archivos con el tag especificado
        else:
            for option in final_filter:  # recorre  cada lista de opciones de tags almacenadas en final_filter
                if option[0] == specified:  # compara que opcion de tag es la especificada por el usuario
                    """imprime unicamente los datos con la especificacion
                    del tag ingresada"""
                    print(tag, option[0], ":")
                    for n in range(1, len(
                            option)):  # recorre la opcion de tag especificada por el usuario desde el indice 1 al ultimo
                        print("     --", option[n])  # imprime los elementos recorridos
                    print("\n")


# ------------------------------------------------PLAYLIST-----------------------------------------------------

def createAlbum(type_file, album_name):
    tags = [album_name]
    saveTags(tags, "album_" + type_file)


def removeToALbum(type_file, album_name, file_name):
    data_albums = readTags("album_" + type_file)

    for albums in data_albums:
        if albums[0] == album_name:
            if file_name in albums:
                albums.remove(file_name)
                saveAllTags(data_albums, "album_" + type_file)
                return None

            else:
                print("no se encontro")

    print("El album no existe")


def addToAlbum(type_file, album_name, file_list):
    res = None
    functions = {'photo': readPhoto, 'music': readMusic, 'video': readVideo}

    not_found = list(file_list)
    found = []

    data = readTags(type_file)

    for file in data:

        if file["file_name"] in file_list:
            not_found.remove(file["file_name"])
            found.append(file["file_name"])

    if len(not_found) != 0:
        for x in not_found:
            functions[type_file](x)
            found.append(x)

    data_albums = readTags("album_" + type_file)

    for albums in data_albums:
        if albums[0] == album_name:
            for file in found:
                albums.append(file)
            saveAllTags(data_albums, "album_" + type_file)
            print("añadido exitosamente")
            return None

    print("El album no existe")


def showAlbum(type_file, album_name):
    album_files = []
    nombre = {'photo': 'album', 'music': 'playlist', 'video': 'playlist'}

    data = readTags(type_file)
    data_albums = readTags("album_" + type_file)

    for albums in data_albums:
        if albums[0] == album_name:
            for x in albums[1:]:
                album_files.append(x)

    print(nombre[type_file], ":", album_name)
    for file in data:
        if file["file_name"] in album_files:
            print("\t" + file["title"][0])


def showAllAlbums(type_file):
    albums = readTags("album_" + type_file)
    nombre = {'photo': 'albumes', 'music': 'playlist', 'video': 'playlist'}

    if len(albums) == 0:
        print("No hay albumes")

    else:

        list_albumes = []
        print("sus " + nombre[type_file] + "son: ")
        for album in albums:  # Recorre todos los albumes ya creados y los guarda en una lista
            print("--- ", album[0])
            list_albumes.append(album[0])

        return list_albumes


def deleteAlbum(type_file, album_name):
    data = readTags("album_" + type_file)
    flag=0
    for album in data:
        if album[0] == album_name:
            flag=1
            data.remove(album)
            saveAllTags(data, "album_" + type_file)
            print("eliminado exitosamente")
            return 0
    if flag==0:
        print("No se encontro playlist")



def search(locking_for,
           lib):  # la funcion recorre las 3 listas de diccionarios y muestra los diccioarios que contengan la expresión que se busca
    found = []
    count = 0
    try:
        for x in readTags(lib):
            for lista in x.values():
                if locking_for in str(lista):
                    if x not in found:
                        found.append(x)
                        count = count + 1
                        print("Nombre: ", x["title"], sep="  ")
                        print("Informacion:")
                        print(x["artist"], x["album"], x["date"], sep="\n")
                        print("--------------------------------------------")
                        print("--------------------------------------------")
    except:
        pass
    return count


# Funcion para definir la interfaz grafica


# --------------------------------------------------------INTERFAZ--------------------------------------------------------

def option():
    """funcion que despliega el menú principal y determina
    la siguiente accion a realizar apartir de la respuesta
    del usuario"""
    while True:
        print(""" Menú principal
        opciones:
///////////////////////////////
    - m ----- Ir a música
    - f ----- Ir a fotos
    - v ----- Ir a videos
    - q ----- Salir
///////////////////////////////
    """)
        # musica
        answer = input()  # almacena en una variable la respuesta del usuario
        if answer == "m":
            seccion = 'music'  # si la respuesta es "m" la seccion a acceder es musica y lo almacena en una varibale
            opciones(seccion)  # ejecuta el menú correspondiente a la seccion

        # seccion videos
        elif answer == "v":
            seccion = 'video'  # si la respuesta es "v" la seccion a acceder es video y lo almacena en una varibale
            opciones(seccion)  # ejecuta el menú correspondiente a la seccion


        # seccion fotos
        elif answer == "f":
            seccion = 'photo'  # si la respuesta es "f" la seccion a acceder es fotos y lo almacena en una varibale
            opciones_fotos(seccion)  # ejecuta el menú correspondiente a la seccion


        elif answer == "q":  # si la respuesta es "q" el usuario finalizar el programa, y el programa se detiene
            print("""
            Hasta Luego
            """)
            return False

        else:  # si la respuesta ingresada es erronea, se le pide al usuario ingresar de nuevo su respuesta
            print("La opcion es incorrecta, ingresela de nuevo")


def opciones(seccion):
    """funcion que despliega el menú para musica y videos y
    determina la siguiente accion a realizar de acuerdo a la
    respuesta del usuario"""
    while True:
        print("   Se encuentra en la seccion de " + seccion + """ ¿Qué desea realizar?
            /////////////////////////
            - b ---- Buscar
            - m ----- Mostrar todos los archivos
            - a ----- Agregar archivo
            - f ----- Filtrar
            - r ----- Reproducir archivo
            - rt ----- Reproducir todo
            - p ----- ir a playlist
            - el ----- Eliminar archivos
            - ell ---- Eliminar todos los archivos de está sección
            - e ----- Regresar a la seccion anterior
            /////////////////////////
            """)

        answer = input()  # almacena en una variable la respuesta del ususario
        if answer == "b":  # si la respuesta es "b", se ejecuta la funcion searching
            searching = input(""""
            Menu de busqueda
            Por favor escriba la expreción que desea busacar en esta seccion: """)
            result = search(searching, seccion)
            print("Se encontraron " + str(result) + " resultados")



        elif answer == "m":  # si la respuesta es "m" muestra los archivos de la seccion
            if seccion == 'music':  # si la seccion es "music" muestra los archivos de esa seccion
                try:
                    allSongs = readTags('music')
                    print("""
                    Sus canciones son:
                    """)
                    print("--------------------------------------------")
                    print("--------------------------------------------")
                    for x in allSongs:
                        print("Name: ", x["title"], sep="  ")
                        print("Data:")
                        print(x["artist"], x["album"], x["date"], sep="\n")
                        print("--------------------------------------------")
                        print("--------------------------------------------")

                except:
                    print("No hay elementos")


            elif seccion == 'video':  # si la seccion es "video" muestra los archivos de esa seccion
                try:
                    allVideos = readTags('video')
                    print("""
                    Sus videos son:
                    """)

                    print("--------------------------------------------")
                    print("--------------------------------------------")
                    for x in allVideos:
                        print("Name: ", x["title"], sep="  ")
                        print("Data:")
                        print(x["artist"], x["album"], x["date"], sep="\n")
                        print("--------------------------------------------")
                        print("--------------------------------------------")
                except:
                    print("No hay elementos")
        elif answer == "a":

            """si la respuesta es "a" el usuario desea añadir archivos,entonces se
            determina la seccion correspondiente y se ejecuta la funcion de esta seccion
            para añadir archivos"""

            name_file = input("escriba la ruta del archivo que desea añadir: ")

            if seccion == 'music':

                if os.path.isfile(name_file) == True:  # verifica si la ruta del archvo existe
                    readMusic(name_file)
                else:
                    print("Error de carga de archivo,verifique la ruta")


            elif seccion == 'video':

                if os.path.isfile(name_file) == True:  # verifica si la ruta del archvo existe
                    readVideo(name_file)
                else:
                    print("Error de carga de archivo,verifique la ruta")


        elif answer == "f":  # si la respuesta es "f" se ejecuta la funcion del menú de filtrado
            filtrado(seccion)

        elif answer == "r":  # opciones aún no disponibles
            print("esta funcion estará disponible proximamente")


        elif answer == "rt":

            print("esta funcion estará disponible proximamente")  # opciones aún no disponibles


        elif answer == "p":  # si la respuesta es "p" se ejecuta la funcion con las opciones de playlist
            option_l_reproduccion(seccion)

        elif answer == "el":  # si la respuesta es "el" el usuario desea eliminar un archivo
            try:
                file_path = input("ruta del archivo")  # se almacena la ruta de archivo ingresada por el usuario
                type_file = input("tipo de archivo")  # se almacena el tipo de archivo ingresado por el usuario
                deleteTags(file_path, type_file)  # se ejecuta la funcion para eliminar archivos
                print("se eliminó el archivo")
            except:
                print("error en la eliminacion")

        elif answer == "ell":
            destroy_info(seccion)  # la respuesta ell borra el pickle perteneciente al tipo de archivo


        elif answer == "e":  # si la respuesta es "e" el usuario desea regresar, y se ejecuta el menú anterior

            break

        else:
            print(
                "la opcion es incorrecta, ingresela de nuevo")  # si la respuesta es incorrecta, el usuario debe ingresar de nuevo la respuesta


def opciones_fotos(seccion):
    """funcion que despliega el menú para la seccion fotos y determina
    la siguiente accion a realizar deacuerdo a la respuesta del usuario"""

    while True:
        print("   se encuentra en la seccion de " + seccion + """ ¿Qué desea realizar?
        /////////////////////////
            - b ----- Buscar
            - m ----- Mostrar todos los Archivos
            - a ----- Agregar archivo
            - f ----- Filtrar
            - r ----- Mostrar archivo
            - rt ----- Reproducir todo
            - al ----- Ir a albumes
            - el ----- Eliminar archivos
            - ell ---- Eliminar todos los archivos de está sección
            - e ----- Regresar a la seccion anterior
        /////////////////////////
            """)
        answer = input()  # almacena la respuesta del usuario

        if answer == "b":  # si la repsuesta es "b" se ejecuta la función searching
            searching = input("""
            Menu de busqueda
            Por favor escriba la expresión que desea buscar en esta seccion: """)
            results = search(searching, seccion)
            print("Se encontraron " + str(results) + " resultados")

        if answer == "m":  # si la respuesta es "m" se muestra en pantalla los archivos existentes en fotos

            if seccion == 'photo':
                try:
                    allPhotos = readTags('photo')
                    print("""
                    sus Fotos son:
                    """)
                    print("--------------------------------------------")
                    print("--------------------------------------------")
                    for x in allPhotos:
                        print("Name: ", x["title"], sep="  ")
                        print("Data:")
                        print(x["artist"], x["date"], sep="\n")
                        print("--------------------------------------------")
                        print("--------------------------------------------")
                except:
                    print("No hay elementos")

        elif answer == "a":  # si la respuesta es "a" se ejecuta la funcion readPhoto() para añadir el archivo
            # funcion add_file()
            # try:

            name_file = input("escriba la ruta del archivo que desea añadir: ")
            if os.path.isfile(name_file) == True:  # verifica si la ruta del archvo existe
                readPhoto(name_file)
            else:
                print("Error de carga de archivo,verifique la ruta")


        elif answer == "f":  # si la respuesta es "f" se ejecuta la función filtrado() con el fin de filtrar los archivos
            filtrado(seccion)

        elif answer == "r":  # opción aún no disponible

            print("Esta funcion estará disponible proximamente")


        elif answer == "el":  # si la respuesta es "el" se ejecuta la funcion para eliminar archivos
            try:
                file_path = input("ruta del archivo")  # se almacena la ruta de archivo ingresada por el usuario
                type_file = input("tipo de archivo")  # se almacena el tipo de archivo ingresado por el usuario
                deleteTags(file_path, type_file)  # se ejecuta la funcion para eliminar archivos
                print("se eliminó el archivo")
            except:
                print("error en la eliminacion")

        elif answer == "rt":  # opción aún no disponible
            # funcion reproducir todos
            print("Esta funcion estará disponible proximamente")

        elif answer == "al":  # si la respuesta es "al" se ejecuta la funcion que despliega el menú de albumes
            option_album('photo')


        elif answer == "ell":

            destroy_info("photo")  # la respuesta "ell" borra el pickle perteneciente al tipo de archivo


        elif answer == "e":  # si la respuesta es "e" se regresa al menú anterior
            break

        else:  # si la respuesta ingresada es incorrecta, el usuario deberá ingresarla de nuevo
            print("La opcion es incorrecta, ingresela de nuevo")


def option_l_reproduccion(seccion):
    """función que despliega el menú de playlist y determina la acción
    correspondiente"""
    while True:
        print("   Se encuentra en la sección de playlist" + """ ¿Qué desea realizar?
			/////////////////////////
			- a ----- Crear lista de reproduccion
			- r ----- Reproducir lista
            - el ---- Eliminar playlist 
			- ell --- Eliminar todas las playlists
			- o  ---- Abrir playlists
			- e ----- Regresar a la seccion anterior
			/////////////////////////
				  """)
        #
        answer = input()  # almacena la respuesta del usuario
        if answer == "a":  # el usuario desea añadir una playlist
            print("Digite el nombre de playlist que desea crear: ")
            name_playlist = input()  # almacena el nombre de la playlist

            createAlbum(seccion, name_playlist)  # ejecuta la función para crear playlist
            option_each_playlist(name_playlist, seccion)  # ejecuta menú para desplegar opciones para cada playlist
            print("se creó lista de reproducción")

        elif answer == "o":  # el usuario desea abrir su carpeta de playlist

            list_playlist = showAllAlbums(seccion)

            if list_playlist != None:

                name_playlist = input(
                    " a que playlist desea acceder")  # almacena el nombre de la playlist a acceder

                if name_playlist not in list_playlist:  # determina si el nombre de la playlist ingresado no se encuentra en la lista de las playlist existentes
                    print("No existe la playlist")

                else:  # la playlist si existe
                    option_each_playlist(name_playlist,
                                         seccion)  # ejecuta la funcion que despliega el menú individual para cada playlist



        elif answer == "r":  # opción no disponible
            # funcion reproducir lista

            print("Esta función estará disponible proximamente")

        elif answer == "el":

            playlist_name = input("ingrese el nombre de la playlist que desea eliminar: ")
            deleteAlbum(seccion, playlist_name)


        elif answer == "ell":

            destroy_info("album_" + seccion)  # funcion para eliminar playlist


        elif answer == "e":  # el usuario desea regresar al menú anterior
            break

        else:  # si la opcion ingresada es incorrecta el usuario debera ingresar de nuevo la opción
            print("La opción es incorrecta, ingresela de nuevo")


def option_each_playlist(name_playlist, seccion):
    """función que despliega el menú para cada playlist y determina la accion correspondiente"""

    while True:
        print("   Se encuentra en la playlist:  ", name_playlist, """ ¿Qué desea realizar?
			/////////////////////////
			- a ----- Añadir archivo
			- r ----- Reproducir playlist
			- el ----- Eliminar archivo:
			- m  ----- Mostrar archivos
			- e ----- Regresar a la seccion anterior
			/////////////////////////
			""")

        answer = input()  # almacena la respuesta del usuario
        # try:
        if answer == "a":  # el usuario desea añadir un archivo a la playlist
            files_to_add = input(
                """Escriba la ruta de los archivos que desea
                agregar a la playlist separados por comas(,): """).split(",")  # almacena la ruta del archivo a añadir
            for file in files_to_add:

                if os.path.isfile(file) == True:
                    addToAlbum(seccion, name_playlist,
                               files_to_add)  # ejecuta funcion para añadir archivos a la playlist
                else:
                    print("el archivo", file, "no existe")




        elif answer == "r":  # opción no disponible
            print("Esta función estará disponible proximamente")

        elif answer == "el":  # ejecuta función para eliminar archivos
            # funcion eliminar playlist

            file_name = input("ingrese la ruta del archivo que desea eliminar: ")
            removeToALbum(seccion, name_playlist, file_name)


        elif answer == "m":  # el usuario desea mostrar los archivos de la playlist
            # funcion reproducir lista
            showAlbum(seccion, name_playlist)  # imprime los elementos de la playlist

        elif answer == "e":  # se retorna el menú anterior
            break

        else:  # la opción ingresada es incorrecta,deberá ingresarla de nuevo
            print("La opcion es incorrecta, ingresela de nuevo")
    # except:


#			print("ha ocurrido un problema,verifique que la direccion del archivo sea correcta")


def option_album(seccion):
    """Despliega menu de albumes y muestra opciones
       función que despliega el menú de album y determina la accion correspondiente"""

    while True:
        print("   Se encuentra en la seccion de album" + """ ¿que desea realizar?
			/////////////////////////
			- c ----- Crear album
			- o ----- Abrir album
			- ell ----- elimnar albumes
			- e ----- Regresar a la seccion anterior
			/////////////////////////""")

        answer = input()

        if answer == "c":
            name_album = input("Digite el nombre del Album que desea crear: ")
            createAlbum(seccion, name_album)  # entrada "c" crea un album con el nombre que introduzca el usuario
            option_each_album(name_album, seccion)

        elif answer == "o":  # El usuario abre un album ya creado

            list_albumes = showAllAlbums(seccion)

            if list_albumes != None:
                name_album = input(
                    "A qué album desea acceder: ")  # pregunta el album a accceder y posteriormente despliega menu del album

                if name_album not in list_albumes:  # El nombre ingresado del album no existe
                    print("El album no existe")

                else:
                    option_each_album(name_album, seccion)  # Se ejecuta la funcion option_each_album

        # funcion para mostrar el nombre de los albumes
        # funcion abrir album--- le pide el nombre del album

        elif answer == "el":

            playlist_name = input("ingrese el nombre del album que desea eliminar: ")
            deleteAlbum(seccion, playlist_name)


        elif answer == "ell":
            destroy_info("album_" + seccion)  # funcion para eliminar album

        elif answer == "e":
            break  # entrada "e" rompe el while volviendo al menu anterior

        else:
            print("La opción es incorrecta, ingresela de nuevo")  # mensaje de entrada incorrecta


def option_each_album(name_album, seccion):
    """Despliega el menu de un album en especifico y da opciones"""

    while True:
        print("   Se encuentra en su album", name_album, """ ¿Qué desea realizar?
				/////////////////////////
				- a ----- añadir archivo
				- r ----- reproducir album
				- m ----- mostrar archivos
				- el ----- Eliminar archivo:
				- e ----- regresar a la seccion anterior
				/////////////////////////
				  """)

        answer = input()
        if answer == "a":  # el usuario desea añadir un archivo a la playlist
            files_to_add = input(
                """Escriba la ruta de los archivos que desea
                agregar a la playlist separados por comas(,): """).split(",")  # almacena la ruta del archivo a añadir
            for file in files_to_add:

                if os.path.isfile(file) == True:
                    addToAlbum(seccion, name_album, files_to_add)
                else:
                    print("el archivo", file, "no existe")




        elif answer == "r":  # opción no disponible
            print("Esta función estará disponible proximamente")

        elif answer == "el":  # ejecuta función para eliminar archivos
            # funcion eliminar playlist

            file_name = input("ingrese la ruta del archivo que desea eliminar: ")
            removeToALbum(seccion, name_album, file_name)



        elif answer == "m":  # el usuario desea mostrar los archivos de la playlist
            # funcion reproducir lista
            showAlbum(seccion, name_album)  # imprime los elementos de la playlist

        elif answer == "e":  # se retorna el menú anterior
            break

        else:  # la opción ingresada es incorrecta,deberá ingresarla de nuevo
            print("La opcion es incorrecta, ingresela de nuevo")


def filtrado(seccion):
    """función que despliega el menú de filtrado y determina la accion correspondiente"""

    while True:
        print("""
                    Se encuentra en la seccion de Filtrado
                    /////////////////////////
                    - n ----- Filtrar por Nombre
                    - a ----- Filtrar por Artista
                    - al ----- Filtrar por Album
                    - f ----- Filtrar por Fecha
                    - g ----- Filtrar por género
                    - e ----- Regresar a la seccion anterior
                    /////////////////////////""")

        answer = input()
        try:
            if answer == "n":  # entrada "n" filtra por letra inicial alfabeticamente
                print("""
                    Filtrando por Nombre:
                    """)
                filterBy("title", seccion)

            elif answer == "a":  # entrada "a" ordena los artistas alfabeticamente y muestra archivos
                print("""
                            Filtrando por Artista:
                            """)
                filterBy("artist", seccion)

            elif answer == "al":  # entrada "al" ordena los albumes alfabeticamente y muestra archivos
                print("""
                                Filtrando por Album:
                                """)
                filterBy("album", seccion)

            elif answer == "f":  # entrada "f" ordena las fechas y muestra archivos

                print("""
                                Filtrando por Fecha:
                                """)
                filterBy("date", seccion)

            elif answer == "g":  # entrada "f" ordena las fechas y muestra archivos

                print("""
                                Filtrando por género:
                                """)
                filterBy("genre", seccion)

            elif answer == "e":  # entrada "e" rompe el ciclo para volver al menu anterior
                break

            else:  # la opción ingresada es incorrecta,deberá ingresarla de nuevo
                print("opcion invalida")
        except:  # En caso de que se genere un error al filtrar los videos / audio se imprimirá esto
            print("No hay archivos")


def filtrado_fotos(seccion):
    "función que despliega el menú de filtrado de fotos y determina la accion correspondiente"
    while True:
        print("""
                Se encuentra en la seccion de Filtrado
                /////////////////////////
                - n ----- Filtrar por Nombre
                - a ----- Filtrar por Artista
                - an ----- Filtrar por Fecha
                - e ----- Regresar a la seccion anterior
                /////////////////////////""")

        answer = input()  # El usuario escribe lo que quiere hacer dentro de este menú
        try:
            if answer == "n":  # Se filtra por nombre las fotos ya cargadas
                print("""
                Filtrando por Nombre:
                """)
                filterBy("title", seccion)

            elif answer == "a":  # entrada "a" ordena los artistas alfabeticamente y muestra archivos
                print("""
                            Filtrando por Artista:
                            """)
                filterBy("artist", seccion)

            elif answer == "an":  # entrada "f" ordena las fechas y muestra archivos

                print("""
                                Filtrando por Fecha:
                                """)
                filterBy("date", seccion)
            elif answer == "e":  # Se retorna el menú anterior
                break

            else:  # la opción ingresada es incorrecta,deberá ingresarla de nuevo
                print("Opción invalida")

        except:  # En caso de que se genere un error al filtrar las fotos se imprimirá esto
            print("No hay archivos")


if __name__ == '__main__':

    pickle_files = {'photo': 'fotos.pickle', 'music': 'musica.pickle', 'video': 'videos.pickle',
                    'album_music': 'album_music.pickle', 'album_photo': 'album_photo.pickle',
                    'album_video': 'album_video.pickle'}

    for t in pickle_files.keys():
        if not os.path.exists(pickle_files[t]):  # comprueba que los pickles existan de no ser asi son creados
            createPickles(t)
            print("creando " + t)

    print("""
    **** Bienvenido a su administrador de archivos *****
    """)  # caluroso mensaje de bienvenida
    option()
