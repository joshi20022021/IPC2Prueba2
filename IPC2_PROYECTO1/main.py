import os
import tkinter as tk
from tkinter import filedialog
import pygame
from cancion import Cancion
from nodo import Nodo
import xml.etree.ElementTree as ET
class ReproductorMusica:
    def __init__(self, ventana):
        self.lista_canciones = None  
        self.cancion_actual = None  

    class ReproductorMusica:
        def __init__(self, ventana):
            self.ventana = ventana
            self.ventana.title("Reproductor de Música")
            self.ventana.geometry("1280x450")  # Modificar el tamaño de la ventana

            self.lista_canciones = []  # Lista de rutas de archivos mp3
            self.indice_cancion_actual = 0

            self.inicializar_gui()

        def inicializar_gui(self):
            self.etiqueta_cancion = tk.Label(self.ventana, text="", font=("Arial", 12), fg="blue")
            self.etiqueta_cancion.pack(pady=10)

            self.frame_botones = tk.Frame(self.ventana, bg="lightgray", height=50)
            self.frame_botones.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)
            
            self.label_tiempo_transcurrido = tk.Label(self.frame_botones, text="0:00", font=("Arial", 8), fg="black")
            self.label_tiempo_transcurrido.pack(side=tk.LEFT, padx=5)

            self.barra_progreso = tk.Scale(self.frame_botones, from_=0, to=100, orient=tk.HORIZONTAL, length=200, showvalue=0, command=self.actualizar_progreso)
            self.barra_progreso.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=False)

            self.label_tiempo_total = tk.Label(self.frame_botones, text="0:00", font=("Arial", 8), fg="black")
            self.label_tiempo_total.pack(side=tk.LEFT, padx=5)

            estilo_boton = {"font": ("Arial", 10),"bg": "lightblue","fg": "white","relief": "raised","width": 12,"height": 2,"bd": 3,"padx": 5,"pady": 5}

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

            self.boton_atras = tk.Button(self.frame_botones, text="Atrás", command=self.cancion_anterior, **estilo_boton)
            self.boton_atras.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=False)

            self.boton_siguiente = tk.Button(self.frame_botones, text="Siguiente", command=self.cancion_siguiente, **estilo_boton)
            self.boton_siguiente.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=False)

            self.ventana.configure(bg="lightgray")

        def cargar_canciones(self):
            archivos = filedialog.askopenfilenames(filetypes=[("Archivos de audio", "*.mp3")])

            self.lista_canciones.extend(archivos)

            if not pygame.mixer.music.get_busy() and self.lista_canciones:
                self.play()

        def cargar_xml(self):
            archivo_xml = filedialog.askopenfilename(title="Selecciona un archivo XML", filetypes=[("Archivos XML", "*.xml")])

            if archivo_xml:
                tree = ET.parse(archivo_xml)
                root = tree.getroot()

                self.lista_canciones = None  # Reiniciar la lista al cargar un nuevo archivo
                self.cancion_actual = None  # Reiniciar la canción actual

                for cancion_elem in root.findall('cancion'):
                    nombre = cancion_elem.get('nombre')
                    artista = cancion_elem.findtext('artista')
                    album = cancion_elem.findtext('album')
                    imagen = cancion_elem.findtext('imagen')
                    ruta = cancion_elem.findtext('ruta')

                    nueva_cancion = Cancion(nombre, artista, album, imagen, ruta)

                    if self.lista_canciones is None:
                        self.lista_canciones = nueva_cancion
                        self.cancion_actual = nueva_cancion
                    else:
                        actual = self.lista_canciones
                        while actual.siguiente:
                            actual = actual.siguiente
                        actual.siguiente = nueva_cancion
                        nueva_cancion.anterior = actual

                if self.lista_canciones:
                    pygame.mixer.init()
                    if not pygame.mixer.music.get_busy():
                        self.play()
            else:
                print("No se seleccionó ningún archivo XML")

        def play(self):
            if self.cancion_actual:
                ruta_cancion = self.cancion_actual.ruta
                pygame.mixer.init()
                pygame.mixer.music.load(ruta_cancion)
                pygame.mixer.music.play()
                self.etiqueta_cancion.config(text=os.path.basename(ruta_cancion))
                self.duracion_cancion = pygame.mixer.Sound(ruta_cancion).get_length()
                self.barra_progreso.config(to=self.duracion_cancion * 1000)  
                
                # Sección añadida para actualizar el tiempo transcurrido y total de la canción
                minutos, segundos = divmod(self.duracion_cancion, 60)
                self.label_tiempo_total.config(text=f"{int(minutos)}:{int(segundos):02}")

                self.actualizar_tiempo()

        def actualizar_tiempo(self):
                if pygame.mixer.music.get_busy():
                    tiempo_actual = pygame.mixer.music.get_pos() / 1000
                    minutos, segundos = divmod(tiempo_actual, 60)
                    self.label_tiempo_transcurrido.config(text=f"{int(minutos)}:{int(segundos):02}")
                    self.barra_progreso.set(tiempo_actual * 1000)
                    self.ventana.after(1000, self.actualizar_tiempo)  # Llama a la función cada segundo

        def actualizar_progreso(self, valor):
                tiempo_actual = int(valor) / 1000 
                pygame.mixer.music.set_pos(tiempo_actual)

        def pause(self):
            pygame.mixer.music.pause()

        def stop(self):
            pygame.mixer.music.stop()

        def cancion_anterior(self):
            if self.cancion_actual and self.cancion_actual.anterior:
                self.cancion_actual = self.cancion_actual.anterior
            else:
                # Si estamos en la primera canción, ir a la última
                while self.cancion_actual.siguiente:
                    self.cancion_actual = self.cancion_actual.siguiente

            self.play()

        def cancion_siguiente(self):
            if self.cancion_actual and self.cancion_actual.siguiente:
                self.cancion_actual = self.cancion_actual.siguiente
            else:
                # Si estamos en la última canción, ir a la primera
                while self.cancion_actual.anterior:
                    self.cancion_actual = self.cancion_actual.anterior

            self.play()

    if __name__ == "__main__":
        ventana_principal = tk.Tk()
        reproductor = ReproductorMusica(ventana_principal)
        ventana_principal.mainloop()