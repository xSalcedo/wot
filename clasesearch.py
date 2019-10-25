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
