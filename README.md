# Detector de Atención con Cámara

Este proyecto es una aplicación que utiliza una cámara para detectar si una persona está procrastinando o no. La aplicación también permite seleccionar una alarma que se activará si el usuario no esta mirando a la pantalla.

## Características

- Selección de cámara disponible para el análisis.
- Elección entre diferentes sonidos de alarma.
- Detección en tiempo real de la dirección de la mirada usando la biblioteca MediaPipe.
- Activación de una alarma sonora si el usuario no está mirando hacia la pantalla.
- Interfaz gráfica de usuario simple creada con Tkinter.

## Requisitos

Antes de ejecutar la aplicación, asegúrate de tener instaladas las siguientes dependencias:

- Python 3.x
- OpenCV
- MediaPipe
- Pillow
- pygame
- Tkinter (incluido por defecto en Python)

Puedes instalar las dependencias necesarias utilizando pip:

```bash
pip install opencv-python mediapipe pillow pygame
