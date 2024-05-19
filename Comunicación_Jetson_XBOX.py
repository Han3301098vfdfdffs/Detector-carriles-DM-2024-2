import serial
import time
import pygame

espera = 2
servo = 1
paso = 10
pwmMax = 120  # Cambia este valor según tu necesidad
pwmMin = 70
velocidad = 0
direccion = 180
        
def go(velocidad):
    if velocidad > pwmMin:
        arduino.write(f'1:0:{velocidad}:{velocidad}:{direccion}\n'.encode())
    #elif velocidad <= 40:
    #    stop()
    else:
        velocidad = pwmMin
        arduino.write(f'1:0:{velocidad}:{velocidad}:{direccion}\n'.encode())

def stop():
    global velocidad
    arduino.write(f'1:0:0:0:{direccion}\n'.encode())
    velocidad = 0

def sleep(espera):
    arduino.write(f'1:0:0:0:{direccion}\n'.encode())
    time.sleep(espera)
    if velocidad > pwmMin:
        arduino.write(f'1:0:{velocidad}:{velocidad}:{direccion}\n'.encode())
    else:
        arduino.write(f'1:0:{pwmMin}:{pwmMin}:{direccion}\n'.encode())

def increase(paso):
    global velocidad
    if velocidad + paso <= pwmMax:
        velocidad += paso
    return velocidad

def decrease(paso):
    global velocidad
    if velocidad - paso >= 0:
        velocidad -= paso
    return velocidad

def update_direccion(joystick):
    global direccion
    global velocidad
    pygame.event.pump()
    axis_value = joystick.get_axis(0)  # Cambia el índice del eje según el joystick izquierdo
    mapped_value = int((axis_value + 1) * 90)  # Mapear el rango [-1, 1] a [0, 180]
    direccion = mapped_value
    arduino.write(f'1:0:{velocidad}:{velocidad}:{direccion}\n'.encode())

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
    arduino = serial.Serial('COM4', 115200)
    print("Conexión Establecida con ESP32")
    time.sleep(2)
    joystick = init_controller()

    while True:
        update_direccion(joystick)  # Actualizar la dirección constantemente
        for event in pygame.event.get():
            try:
                if event.type == pygame.JOYHATMOTION:
                    if event.value == (0, 1):  # Flecha arriba
                        increase(10)
                    elif event.value == (0, -1):  # Flecha abajo
                        decrease(10)
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        go(velocidad)
                        print("Botón A presionado")
                    elif event.button == 1:
                        stop()
                        print("Botón B presionado")
                    elif event.button == 2:
                        sleep(espera)
                        print("Botón X presionado")
                    elif event.button == 8:
                        velocidad = 90
                        go(velocidad)
                        print("Botón LS presionado")
                    elif event.button == 9:
                        velocidad = 180
                        go(velocidad)
                        print("Botón RS presionado")
            except Exception as e:
                print(f"Error: {e}")

        print(f'{velocidad}  {direccion}')
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
