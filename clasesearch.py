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


def search(self, locking_for, lib):
	self.found = []
    self.count = 0
	self.lib = lib
	self.locking_for = locking_for
    try:
        for x in readTags(self.lib):
            for lista in x.values():
                if self.locking_for in str(lista):
                    if x not in self.found:
                        self.found.append(x)
                        self.count = self.count + 1
                        print("Nombre: ", x["title"], sep="  ")
                        print("Informacion:")
                        print(x["artist"], x["album"], x["date"], sep="\n")
                        print("--------------------------------------------")
                        print("--------------------------------------------")
	except:
        pass
    return count






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
