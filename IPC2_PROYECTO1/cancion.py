from nodo import Nodo

class Cancion:
    def __init__(self, nombre, artista, album, imagen, ruta):
        self.nombre = nombre
        self.artista = artista
        self.album = album
        self.imagen = imagen
        self.ruta = ruta
        self.nodo = Nodo(self)
        self.siguiente = None
        self.anterior = None

