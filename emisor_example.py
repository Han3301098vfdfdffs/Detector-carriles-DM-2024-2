import socket
import random

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
        while True:
            # Generar un valor aleatorio para enviar
            direccion = random.randint(1, 100)
            print(f"Enviando dirección aleatoria: {direccion}")
            conn.sendall(str(direccion).encode())
