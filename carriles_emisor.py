import numpy as np
import cv2
import utils
import socket

cameraFeed = True
cameraNo = 1
frameWidth = 1280
frameHeight = 720
factortamano = 3  # Definir la resolución
TAMANO_IMG = 256  # Definir el tamaño de la imagen
cambio_bn = 0  # 1 para convertir a blanco y negro, 0 para mantener el color original

# Valores iniciales de la barra de seguimiento
if cameraFeed:
    intialTracbarVals = [40, 63, 8, 92]  # test5
else:
    intialTracbarVals = [42, 63, 14, 87]  # wT,hT,wB,hB

# Configuración del feed de la cámara o video
if cameraFeed:
    cap = cv2.VideoCapture('test4.mp4')
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)

count = 0
noOfArrayValues = 10
global arrayCurve, arrayCounter
arrayCounter = 0
arrayCurve = np.zeros([noOfArrayValues])
myVals = []
utils.initializeTrackbars(intialTracbarVals)

# Configuración del socket
HOST = '192.168.1.70'  # Dirección IP del servidor
PORT = 65432        # Puerto de comunicación

# Crear un socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Conectado al servidor")

    while True:
        success, img = cap.read()
        if not success:
            break

        # Reducir la resolución de la imagen
        reduced_width = frameWidth // factortamano
        reduced_height = frameHeight // factortamano
        img = cv2.resize(img, (reduced_width, reduced_height))

        # Copias de la imagen para diferentes operaciones
        imgWarpPoints = img.copy()
        imgFinal = img.copy()
        imgCanny = img.copy()

        # Procesamiento de la imagen
        imgUndis = utils.undistort(img)
        imgThres, imgCanny, imgColor = utils.thresholding(imgUndis)
        src = utils.valTrackbars()
        imgWarp = utils.perspective_warp(imgThres, dst_size=(reduced_width, reduced_height), src=src)
        imgWarpPoints = utils.drawPoints(imgWarpPoints, src)
        imgSliding, curves, lanes, ploty = utils.sliding_window(imgWarp, draw_windows=True)

        try:
            curverad = utils.get_curve(imgFinal, curves[0], curves[1])
            lane_curve = np.mean([curverad[0], curverad[1]])
            imgFinal = utils.draw_lanes(img, curves[0], curves[1], reduced_width, reduced_height, src=src)

            currentCurve = lane_curve // 50
            if int(np.sum(arrayCurve)) == 0:
                averageCurve = currentCurve
            else:
                averageCurve = np.sum(arrayCurve) // arrayCurve.shape[0]
            if abs(averageCurve - currentCurve) > 200:
                arrayCurve[arrayCounter] = averageCurve
            else:
                arrayCurve[arrayCounter] = currentCurve
            arrayCounter += 1
            if arrayCounter >= noOfArrayValues:
                arrayCounter = 0

            # Enviar el valor de averageCurve al servidor
            direccion = utils.mapeo(averageCurve, 90, 100, -100)
            direccion = int(direccion)
            data = str(direccion).encode()
            s.sendall(data)
            print(data)

            cv2.putText(imgFinal, str(int(averageCurve)), (reduced_width // 2 - 70, 70), cv2.FONT_HERSHEY_DUPLEX, 1.75,
                        (0, 0, 255), 2, cv2.LINE_AA)
        except Exception as e:
            lane_curve = 0
            print(e)

        imgFinal = utils.drawLines(imgFinal, lane_curve)

        imgThres = cv2.cvtColor(imgThres, cv2.COLOR_GRAY2BGR)
        imgBlank = np.zeros_like(img)
        imgStacked = utils.stackImages(0.7, ([img, imgUndis, imgWarpPoints, imgColor, imgCanny],
                                             [imgThres, imgWarp, imgSliding, imgFinal, imgFinal],
                                             ))

        if cambio_bn == 1:
            # Cambiar tamaño de la imagen imgFinal
            imgFinal = cv2.resize(imgFinal, (TAMANO_IMG, TAMANO_IMG))
            # Convertir la imagen imgFinal a blanco y negro
            imgFinal = cv2.cvtColor(imgFinal, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("imgWarpPoints", imgWarpPoints)
        #cv2.imshow("imgSliding", imgSliding)
        cv2.imshow("imgFinal", imgFinal)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
