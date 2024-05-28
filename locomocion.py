import serial
import time
import pygame
import numpy as np

def moving_average(data, window_size):
    if len(data) < window_size:
        return np.mean(data)
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')[-1]

def fir_filter(data, coefficients):
    if len(data) < len(coefficients):
        return np.dot(data, coefficients[:len(data)])
    return np.dot(data[-len(coefficients):], coefficients)

def iir_filter(data, b, a):
    if len(data) < max(len(b), len(a)):
        return data[-1] if data else 0
    y = np.zeros(len(data))
    for i in range(len(data)):
        y[i] = b[0] * data[i]
        for j in range(1, len(b)):
            if i - j >= 0:
                y[i] += b[j] * data[i - j]
        for j in range(1, len(a)):
            if i - j >= 0:
                y[i] -= a[j] * y[i - j]
    return y[-1]

class KalmanFilter:
    def __init__(self, process_variance, measurement_variance, estimated_measurement_variance):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.estimated_measurement_variance = estimated_measurement_variance
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0

    def update(self, measurement):
        priori_estimate = self.posteri_estimate
        priori_error_estimate = self.posteri_error_estimate + self.process_variance

        blending_factor = priori_error_estimate / (priori_error_estimate + self.measurement_variance)
        self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
        self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate

        return self.posteri_estimate

def downsample(data, factor):
    return data[::factor]
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

direccion_data = []

# Inicialización del filtro Kalman
kf = KalmanFilter(process_variance=1e-5, measurement_variance=0.1**2, estimated_measurement_variance=1.0)

# Inicialización de coeficientes para FIR e IIR
fir_coefficients = [0.1, 0.15, 0.5, 0.15, 0.1]
iir_b = [0.1, 0.15, 0.5, 0.15, 0.1]  # Numerador
iir_a = [1, -0.85]  # Denominador

# Variables para almacenar los valores anteriores
prev_in1, prev_in2 = in1, in2
prev_velocidad1, prev_velocidad2 = velocidad1, velocidad2
prev_direccion = direccion

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

def update_direccion(joystick):
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

def init_controller():
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return joystick

def read_joystick(joystick):
    pygame.event.pump()
    axis_value = joystick.get_axis(2)
    mapped_value = int(axis_value * servo)
    return mapped_value

try:
    arduino = serial.Serial('/dev/ttyUSB0', 115200)  # LINUX
    # arduino = serial.Serial('COM8', 115200) #WINDOWS
    print("Conexión Establecida con ESP32")
    time.sleep(2)
    joystick = init_controller()

    while True:
        update_direccion(joystick)  # Actualizar la dirección constantemente
        for event in pygame.event.get():
            try:
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
                elif event.type == pygame.JOYBUTTONDOWN:
                    print("Botón A presionado")
                    if event.button == 0:
                        vel(pwmMin, pwmMin)
                    elif event.button == 1:
                        print("Botón B presionado")
                        vel(0, 0)
                    elif event.button == 2:
                        print("Botón X presionado")
                        sleep(espera)
                    elif event.button == 3:
                        print("Botón Y presionado")
                        vel(pwmMax, pwmMax)
                    elif event.button == 4:
                        print("WARNING")
                        desviar()
            except Exception as e:
                print(f"Error: {e}")
        if (in1 != prev_in1 or in2 != prev_in2 or velocidad1 != prev_velocidad1 or velocidad2 != prev_velocidad2 or direccion != prev_direccion):
            actualizar()
            prev_in1, prev_in2 = in1, in2
            prev_velocidad1, prev_velocidad2 = velocidad1, velocidad2
            prev_direccion = direccion
        time.sleep(0.1)

except serial.SerialException as e:
    print('Error al abrir puerto serial:', e)
except pygame.error as e:
    print('Error al inicializar el controlador:', e)
finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()
        print("Conexión cerrada con la ESP32")
    pygame.quit()
