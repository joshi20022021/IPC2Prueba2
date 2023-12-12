import os
import tkinter as tk
from tkinter import filedialog
import pygame
from cancion import Cancion
from nodo import Nodo
from cancion import ReproductorMusica
import xml.etree.ElementTree as ET

class ReproductorMusica:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Reproductor de Música")
        self.ventana.geometry("680x450")  # Modificar el tamaño de la ventana

        self.lista_canciones = []  # Lista de rutas de archivos mp3
        self.indice_cancion_actual = 0

        self.inicializar_gui()

    def inicializar_gui(self):
        # Etiqueta para mostrar el nombre de la canción actual
        self.etiqueta_cancion = tk.Label(self.ventana, text="", font=("Arial", 12), fg="blue")
        self.etiqueta_cancion.pack(pady=10)

        # Frame para la barra inferior con altura de 50px
        self.frame_botones = tk.Frame(self.ventana, bg="lightgray", height=50)
        self.frame_botones.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

        # Estilo para los botones
        estilo_boton = {
            "font": ("Arial", 10),
            "bg": "lightblue",
            "fg": "white",
            "relief": "raised",
            "width": 12,
            "height": 2,
            "bd": 3,
            "padx": 5,
            "pady": 5
        }

        # Botones en el frame de la barra inferior
        self.boton_cargar = tk.Button(self.frame_botones, text="Cargar Canciones", command=self.cargar_canciones, **estilo_boton)
        self.boton_cargar.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=False)

        self.boton_cargar_xml = tk.Button(self.frame_botones, text="Cargar XML", command=self.cargar_xml, **estilo_boton)
        self.boton_cargar_xml.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=False)

        self.boton_play = tk.Button(self.frame_botones, text="Play", command=self.play, **estilo_boton)
        self.boton_play.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=False)

        self.boton_pause = tk.Button(self.frame_botones, text="Pause", command=self.pause, **estilo_boton)
        self.boton_pause.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=False)

        self.boton_stop = tk.Button(self.frame_botones, text="Stop", command=self.stop, **estilo_boton)
        self.boton_stop.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=False)

        

        # Cambiar el color de fondo de la ventana
        self.ventana.configure(bg="lightgray")

    def cargar_canciones(self):
        # Abre el diálogo para seleccionar archivos de música
        archivos = filedialog.askopenfilenames(filetypes=[("Archivos de audio", "*.mp3")])

        # Agrega las canciones a la lista
        self.lista_canciones.extend(archivos)

        # Inicia la primera canción si no hay ninguna reproduciéndose
        if not pygame.mixer.music.get_busy() and self.lista_canciones:
            self.play()

    def cargar_xml(self):

        archivo_xml = filedialog.askopenfilename(title="Selecciona un archivo XML", filetypes=[("Archivos XML", "*.xml")])

        if archivo_xml:
            
            tree = ET.parse(archivo_xml)
            root = tree.getroot()


            lista_canciones = None
            canciones = root.findall('cancion')


            for cancion in canciones:
                nombre = cancion.get('nombre')
                artista = cancion.findtext('artista')
                album = cancion.findtext('album')
                imagen = cancion.findtext('imagen')
                ruta = cancion.findtext('ruta')


                if artista is not None and album is not None and imagen is not None and ruta is not None:
                    nueva_cancion = Cancion(nombre, artista, album, imagen, ruta)
                    

                    if lista_canciones is None:
                        lista_canciones = nueva_cancion
                    else:
                        actual = lista_canciones
                        while actual.nodo.siguiente:
                            actual = actual.nodo.siguiente.data
                        actual.nodo.siguiente = Nodo(nueva_cancion)
                        actual.nodo.siguiente.anterior = actual.nodo


            actual = lista_canciones
            while actual:
                print(f"Nombre: {actual.nombre}, Artista: {actual.artista}, Album: {actual.album}, Imagen: {actual.imagen}, Ruta: {actual.ruta}")
                siguiente = actual.nodo.siguiente
                if siguiente:
                    actual = siguiente.data
                else:
                    break


            ultimo = actual
            while ultimo:
                anterior = ultimo.nodo.anterior
                if anterior:
                    ultimo = anterior.data
                else:
                    break

            while ultimo:
                print(f"Nombre: {ultimo.nombre}, Artista: {ultimo.artista}, Album: {ultimo.album}, Imagen: {ultimo.imagen}, Ruta: {ultimo.ruta}")
                siguiente = ultimo.nodo.siguiente
                if siguiente:
                    ultimo = siguiente.data
                else:
                    break

        else:
            print("No se seleccionó ningún archivo XML")

    def play(self):
        if self.lista_canciones:
            pygame.mixer.init()
            pygame.mixer.music.load(self.lista_canciones[self.indice_cancion_actual])
            pygame.mixer.music.play()
            self.etiqueta_cancion.config(text=os.path.basename(self.lista_canciones[self.indice_cancion_actual]))

    def pause(self):
        pygame.mixer.music.pause()

    def stop(self):
        pygame.mixer.music.stop()

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    reproductor = ReproductorMusica(ventana_principal)
    ventana_principal.mainloop()