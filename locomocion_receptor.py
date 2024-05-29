import serial
import time
import pygame
import numpy as np
import socket

#------------------------------------------------------------------------------------------------
espera = 2
servo = 1
paso = 10
pwmMax = 200  # Cambia este valor según tu necesidad
pwmMin = 100
velocidad1 = 0
velocidad2 = 0
direccion = 180
in1 = 0
in2 = 0
renaudar1 = 0
renaudar2 = 0
giroderecha = 120
giroizquierda = 40


def go():
    global in1, in2
    in1 = 0
    in2 = 1
    return in1, in2

def reverse():
    global in1, in2
    in1 = 1
    in2 = 0
    return in1, in2

def vel(vel1, vel2):
    global velocidad1, velocidad2
    velocidad1 = vel1
    velocidad2 = vel2
    return velocidad1, velocidad2

def actualizar():
    global in1, in2
    global velocidad1, velocidad2
    global direccion
    arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
    print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())

def sleep(espera):
    global pwmMin
    global velocidad1, velocidad2
    global renaudar1, renaudar2
    if in1 == 0 and in2 == 0:
        go()
        actualizar()
        if (velocidad1 == 0 or velocidad1 <= 40) and (velocidad2 == 0 or velocidad2 <= 40):
            vel(0, 0)
            actualizar()
            time.sleep(espera)
            actualizar()
            vel(pwmMin, pwmMin)
        else:
            renaudar1 = velocidad1
            renaudar2 = velocidad2
            vel(0, 0)
            actualizar()
            time.sleep(espera)
            actualizar()
            vel(renaudar1, renaudar2)

    else:
        if (velocidad1 == 0 or velocidad1 <= 40) and (velocidad2 == 0 or velocidad2 <= 40):
            vel(pwmMin, pwmMin)
            renaudar1 = velocidad1
            renaudar2 = velocidad2
            vel(0, 0)
            actualizar()
            time.sleep(espera)
            actualizar()
            vel(renaudar1, renaudar2)
        else:
            renaudar1 = velocidad1
            renaudar2 = velocidad2
            vel(0, 0)
            actualizar()
            time.sleep(espera)
            actualizar()
            vel(renaudar1, renaudar2)

def rutinaderecha():
    global in1, in2
    global velocidad1, velocidad2
    global pwmMin, direccion
    if in1 == 0 and in2 == 0:
        go()
    vel(0, 0)
    arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroderecha}\n'.encode())
    print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroderecha}\n'.encode())
    time.sleep(1)
    vel(pwmMin, pwmMin)
    arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroderecha}\n'.encode())
    print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroderecha}\n'.encode())
    time.sleep(2)

def rutinaizquierda():
    global in1, in2
    global velocidad1, velocidad2
    global pwmMin, direccion
    if in1 == 0 and in2 == 0:
        go()
    vel(0, 0)
    arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroizquierda}\n'.encode())
    print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroizquierda}\n'.encode())
    time.sleep(1)
    vel(pwmMin, pwmMin)
    arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroizquierda}\n'.encode())
    print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroizquierda}\n'.encode())
    time.sleep(2)

def desviar():
    vel(0,0)
    actualizar()
    time.sleep(1)
    reverse()
    vel(pwmMin, pwmMin)
    actualizar()
    global direccion, direccion_data
    pygame.event.pump()
    axis_value = joystick.get_axis(0)  # Cambia el índice del eje según el joystick izquierdo
    mapped_value = int((axis_value + 1) * 73)  # Mapear el rango [-1, 1] a [0, 180]
    direccion_data.append(mapped_value)

    # Aplicar filtro deseado
    filtered_value = moving_average(direccion_data, window_size=5)
    # filtered_value = fir_filter(direccion_data, fir_coefficients)
    # filtered_value = iir_filter(direccion_data, iir_b, iir_a)
    # filtered_value = kf.update(mapped_value)
    # filtered_value = downsample(direccion_data, factor=2)[-1]  # Submuestreo cada factor lecturas

    direccion = int(filtered_value)
    actualizar()
    return direccion

# Configuración del socket
HOST = '192.168.1.70'  # Dirección IP del servidor
PORT = 65432        # Puerto de comunicación

# Crear un socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Esperando la conexión entrante...")
    conn, addr = s.accept()
    with conn:
        print(f"Conectado a {addr}")
        try:
            arduino = serial.Serial('/dev/ttyUSB0', 115200)  # LINUX
            # arduino = serial.Serial('COM8', 115200) #WINDOWS
            print("Conexión Establecida con ESP32")
            time.sleep(2)

            # Inicializar Pygame y el joystick
            pygame.init()
            pygame.joystick.init()
            joystick = pygame.joystick.Joystick(0)
            joystick.init()

            while True:
                # Capturar eventos de Pygame
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 0:  # Botón A
                            print("Botón A presionado")
                            vel(pwmMin, pwmMin)
                        elif event.button == 1:  # boton B
                            print("Botón B presionado")
                            vel(0, 0)
                        elif event.button == 2:  # boton X
                            print("Botón X presionado")
                            sleep(espera)
                        elif event.button == 3:  # boton Y
                            print("Botón Y presionado")
                            vel(pwmMax, pwmMax)
                        elif event.button == 4:  # boton LB
                            print("WARNING")
                            desviar()
                    if event.type == pygame.JOYHATMOTION:
                        if event.value == (0, -1):  # Flecha arriba
                            print("Reversa")
                            reverse()
                        elif event.value == (0, 1):  # Flecha abajo
                            print("Adelante")
                            go()
                        elif event.value == (-1, 0):  # Flecha abajo
                            print("Izquierda")
                            rutinaizquierda()
                        elif event.value == (1, 0):  # Flecha abajo
                            print("Derecha")
                            rutinaderecha()                
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    value = int(data.decode())
                except ValueError:
                    print("Error al convertir los datos recibidos a entero")
                direccion = value
                
                actualizar()

        except serial.SerialException as e:
            print('Error al abrir puerto serial:', e)
        finally:
            if 'arduino' in locals() and arduino.is_open:
                arduino.close()
                print("Conexión cerrada con la ESP32")