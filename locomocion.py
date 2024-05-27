import serial
import time
import pygame

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
giroizquierda = 60

def sleep(espera):
    global direccion
    global pwmMin
    global in1
    global in2
    global velocidad1
    global velocidad2
    global renaudar1
    global renaudar2
    if in1 == 0 and in2==0:
        in1 = 0
        in2 = 1
        print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
        if (velocidad1 == 0 or velocidad1 <=40) and (velocidad2 == 0 or velocidad2 <=40):
            velocidad1 = pwmMin
            velocidad2 = pwmMin
            renaudar1 = velocidad1
            renaudar2 = velocidad2
            velocidad1 = 0
            velocidad2 = 0
            arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            time.sleep(espera)
            arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            velocidad1 = renaudar1
            velocidad2 = renaudar2
        else:
            renaudar1 = velocidad1
            renaudar2 = velocidad2
            velocidad1 = 0
            velocidad2 = 0
            arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            time.sleep(espera)
            arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            velocidad1 = renaudar1
            velocidad2 = renaudar2
    else:
        if (velocidad1 == 0 or velocidad1 <=40) and (velocidad2 == 0 or velocidad2 <=40):
            velocidad1 = pwmMin
            velocidad2 = pwmMin
            renaudar1 = velocidad1
            renaudar2 = velocidad2
            velocidad1 = 0
            velocidad2 = 0
            arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            time.sleep(espera)
            arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            velocidad1 = renaudar1
            velocidad2 = renaudar2
        else:
            renaudar1 = velocidad1
            renaudar2 = velocidad2
            velocidad1 = 0
            velocidad2 = 0
            arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            time.sleep(espera)
            arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
            velocidad1 = renaudar1
            velocidad2 = renaudar2

def rutinaderecha():
    global in1
    global in2
    global velocidad1
    global velocidad2
    global direccion
    global renaudar1
    global renaudar2
    global giroderecha
    if in1 == 0 and in2 == 0:
        in1 = 0
        in2 = 1
    velocidad1 = 0
    velocidad2 = 0
    arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroderecha}\n'.encode())
    print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroderecha}\n'.encode())
    time.sleep(1)
    velocidad1 = pwmMin
    velocidad2 = pwmMin
    arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroderecha}\n'.encode())
    print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroderecha}\n'.encode())
    time.sleep(2)

    
def rutinaizquierda():
    global in1
    global in2
    global velocidad1
    global velocidad2
    global direccion
    global renaudar1
    global renaudar2
    global giroizquierda
    if in1 == 0 and in2 == 0:
        in1 = 0
        in2 = 1
    velocidad1 = 0
    velocidad2 = 0
    arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroizquierda}\n'.encode())
    print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroizquierda}\n'.encode())
    time.sleep(1)
    velocidad1 = pwmMin
    velocidad2 = pwmMin
    arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroizquierda}\n'.encode())
    print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{giroizquierda}\n'.encode())
    time.sleep(2)

#def increase(paso):
#    global velocidad
#    if velocidad + paso <= pwmMax:
#        velocidad += paso
#    return velocidad

#def decrease(paso):
#    global velocidad
#    if velocidad - paso >= 0:
#        velocidad -= paso
#    return velocidad

def update_direccion(joystick):
    global direccion
    global velocidad1
    global velocidad2
    pygame.event.pump()
    axis_value = joystick.get_axis(0)  # Cambia el índice del eje según el joystick izquierdo
    mapped_value = int((axis_value + 1) * 90)  # Mapear el rango [-1, 1] a [0, 180]
    direccion = mapped_value
    arduino.write(f'1:0:{velocidad1}:{velocidad2}:{direccion}\n'.encode())

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
    arduino = serial.Serial('/dev/ttyUSB0', 115200) #LINUX
    #arduino = serial.Serial('COM8', 115200) #WINDOWS
    print("Conexión Establecida con ESP32")
    time.sleep(2)
    joystick = init_controller()

    while True:
        update_direccion(joystick)  # Actualizar la dirección constantemente
        for event in pygame.event.get():
            try:
                if event.type == pygame.JOYHATMOTION:
                    if event.value == (0, 1):  # Flecha arriba
                        print("Adelante")
                        in1 = 1
                        in2 = 0
                    elif event.value == (0, -1):  # Flecha abajo
                        print("Reversa")
                        in1 = 0
                        in2 = 1
                    elif event.value == (1, 0):  # Flecha abajo
                        print("Derecha")
                        rutinaizquierda()
                    elif event.value == (-1, 0):  # Flecha abajo
                        print("Izquierda")
                        rutinaderecha()
                elif event.type == pygame.JOYBUTTONDOWN:
                    print("Botón A presionado")
                    if event.button == 0:
                        velocidad1 = pwmMin
                        velocidad2 = pwmMin
                    elif event.button == 1:
                        print("Botón B presionado")
                        velocidad1 = 0
                        velocidad2 = 0
                    elif event.button == 2:
                        print("Botón X presionado")
                        sleep(espera)
                    elif event.button == 3:
                        print("Botón Y presionado")
                        velocidad1 = pwmMax
                        velocidad2 = pwmMax
            except Exception as e:
                print(f"Error: {e}")
        arduino.write(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
        print(f'{in1}:{in2}:{velocidad1}:{velocidad2}:{direccion}\n'.encode())
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
