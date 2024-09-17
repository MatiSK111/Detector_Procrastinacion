import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
import numpy as np
import pygame

class SeleccionadorDeCamaras:
    def __init__(self, root):
        self.root = root
        self.root.title("Seleccionar Cámara")
        self.root.geometry("200x200")
        self.root.config(bg='green')
        self.root.resizable(False, False)

        self.camera_index = None
        self.alarma_seleccionada = None
        self.crear_widgets()

    def crear_widgets(self):
        self.lista_de_camaras = ttk.Combobox(self.root)
        self.lista_de_camaras.pack(pady=10)
        self.lista_de_camaras.bind("<<ComboboxSelected>>", self.seleccionar_camara)

        self.lista_de_alarmas = ttk.Combobox(self.root, values=["Alarma 1", "Alarma 2"])
        self.lista_de_alarmas.pack(pady=10)
        self.lista_de_alarmas.bind("<<ComboboxSelected>>", self.seleccionar_alarma)

        tk.Button(self.root, text="Abrir Cámara", command=self.abrir_ventana_camara).pack(pady=10)
        self.actualizar_lista_de_camaras()

    def actualizar_lista_de_camaras(self):
        self.lista_de_camaras['values'] = self.obtener_indices_de_camaras()
        if self.lista_de_camaras['values']:
            self.lista_de_camaras.current(0)

    def obtener_indices_de_camaras(self):
        indices = [i for i in range(5) if cv2.VideoCapture(i).isOpened()]
        return indices

    def seleccionar_camara(self, event):
        self.camera_index = int(self.lista_de_camaras.get())

    def seleccionar_alarma(self, event):
        self.alarma_seleccionada = self.lista_de_alarmas.get()

    def abrir_ventana_camara(self):
        if self.camera_index is not None and self.alarma_seleccionada is not None:
            self.root.withdraw()
            ventana_camara = tk.Toplevel(self.root)
            AplicacionDeCamara(ventana_camara, self.camera_index, self.alarma_seleccionada)
        else:
            print("Selecciona una cámara y una alarma primero.")

class AplicacionDeCamara:
    def __init__(self, root, camera_index, alarma_seleccionada):
        self.root = root
        self.root.title("Cámara")
        self.root.geometry("800x600")
        self.camera_index = camera_index
        self.capture = None
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(max_num_faces=1)
        self.mp_drawing = mp.solutions.drawing_utils

        pygame.mixer.init()
        self.sonido_alarma = pygame.mixer.Sound("ALARMA1.mp3" if alarma_seleccionada == "Alarma 1" else "ALARMA2.mp3")
        self.alarma_reproduciendo = False

        self.crear_widgets()
        self.abrir_camara()

    def crear_widgets(self):
        self.etiqueta_video = tk.Label(self.root, bg='black')
        self.etiqueta_video.pack(expand=True, fill=tk.BOTH)

        self.etiqueta_estado = tk.Label(self.root, text="Mira hacia la pantalla", font=("Helvetica", 16))
        self.etiqueta_estado.pack(pady=10)

    def abrir_camara(self):
        if self.capture:
            self.capture.release()
        self.capture = cv2.VideoCapture(self.camera_index)
        self.actualizar_frame()

    def actualizar_frame(self):
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                resultados = self.mp_face_mesh.process(frame_rgb)

                if resultados.multi_face_landmarks:
                    for landmarks in resultados.multi_face_landmarks:
                        h, w, _ = frame.shape
                        landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks.landmark]

                        for i in range(468):
                            cv2.circle(frame, landmarks[i], 2, (0, 255, 0), -1)
                        
                        indices_ojo_izquierdo, indices_ojo_derecho = range(33, 133), range(362, 463)
                        for i in indices_ojo_izquierdo:
                            cv2.circle(frame, landmarks[i], 2, (255, 0, 0), -1)
                        for i in indices_ojo_derecho:
                            cv2.circle(frame, landmarks[i], 2, (255, 0, 0), -1)

                        ojo_izquierdo = np.mean([landmarks[i] for i in indices_ojo_izquierdo], axis=0)
                        ojo_derecho = np.mean([landmarks[i] for i in indices_ojo_derecho], axis=0)
                        centro_ojos = np.mean([ojo_izquierdo, ojo_derecho], axis=0)

                        centro_cara_x, centro_cara_y = w / 2, h / 2
                        desviacion_x = abs(centro_ojos[0] - centro_cara_x)
                        desviacion_y = abs(centro_ojos[1] - centro_cara_y)

                        if desviacion_x < 50 and desviacion_y < 50:
                            self.etiqueta_estado.config(text="Mirando hacia la pantalla", fg="green")
                            self.etiqueta_video.config(bg='black')
                            if self.alarma_reproduciendo:
                                self.sonido_alarma.stop()
                                self.alarma_reproduciendo = False
                        else:
                            self.etiqueta_estado.config(text="¡MIRA LA PANTALLA!", fg="red")
                            self.etiqueta_video.config(bg='red')
                            if not self.alarma_reproduciendo:
                                self.sonido_alarma.play(-1)
                                self.alarma_reproduciendo = True
                else:
                    self.etiqueta_estado.config(text="No se detecta rostro", fg="red")
                    self.etiqueta_video.config(bg='red')
                    if not self.alarma_reproduciendo:
                        self.sonido_alarma.play(-1)
                        self.alarma_reproduciendo = True

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                imagen = ImageTk.PhotoImage(Image.fromarray(frame))
                self.etiqueta_video.config(image=imagen)
                self.etiqueta_video.image = imagen
        self.root.after(30, self.actualizar_frame)

    def __del__(self):
        if self.capture:
            self.capture.release()
        pygame.quit()

ventana = tk.Tk()
app = SeleccionadorDeCamaras(ventana)
ventana.mainloop()
