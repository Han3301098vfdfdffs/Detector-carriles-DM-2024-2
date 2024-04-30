import numpy as np
import cv2
import utils

cameraFeed = True
cameraNo = 1
frameWidth = 1280
frameHeight = 720

#if cameraFeed:intialTracbarVals = [39, 51, 21, 83] #  test2
#if cameraFeed:intialTracbarVals = [37, 69, 12, 92] #  test4
if cameraFeed:intialTracbarVals = [40, 60, 17, 91] #  test5
else:
    intialTracbarVals = [42, 63, 14, 87]  # wT,hT,wB,hB

if cameraFeed:
    cap = cv2.VideoCapture('test5.mp4')
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)

count = 0
noOfArrayValues = 10
global arrayCurve, arrayCounter
arrayCounter = 0
arrayCurve = np.zeros([noOfArrayValues])
myVals = []
utils.initializeTrackbars(intialTracbarVals)

while True:
    success, img = cap.read()
    imgWarpPoints = img.copy()
    imgFinal = img.copy()
    imgCanny = img.copy()

    imgUndis = utils.undistort(img)
    imgThres, imgCanny, imgColor = utils.thresholding(imgUndis)
    src = utils.valTrackbars()
    imgWarp = utils.perspective_warp(imgThres, dst_size=(frameWidth, frameHeight), src=src)
    imgWarpPoints = utils.drawPoints(imgWarpPoints, src)
    imgSliding, curves, lanes, ploty = utils.sliding_window(imgWarp, draw_windows=True)

    try:
        curverad = utils.get_curve(imgFinal, curves[0], curves[1])
        lane_curve = np.mean([curverad[0], curverad[1]])
        imgFinal = utils.draw_lanes(img, curves[0], curves[1], frameWidth, frameHeight, src=src)

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
        cv2.putText(imgFinal, str(int(averageCurve)), (frameWidth // 2 - 70, 70), cv2.FONT_HERSHEY_DUPLEX, 1.75,
                    (0, 0, 255), 2, cv2.LINE_AA)

        # Llama a textDisplay para mostrar la dirección en la imagen
        utils.textDisplay(averageCurve, imgFinal)

    except Exception as e:
        lane_curve = 0
        print(e)

    imgFinal_resized = cv2.resize(imgFinal, (frameWidth, frameHeight))
    imgFinal = utils.drawLines(imgFinal, lane_curve)

    imgThres = cv2.cvtColor(imgThres, cv2.COLOR_GRAY2BGR)
    imgBlank = np.zeros_like(img)
    imgStacked = utils.stackImages(0.7, ([img, imgUndis, imgWarpPoints, imgColor, imgCanny],
                                         [imgThres, imgWarp, imgSliding, imgFinal, imgFinal],
                                         ))

    #cv2.imshow("imgWarpPoints", imgWarpPoints)
    #cv2.imshow("imgSliding", imgSliding)
    cv2.imshow("imgFinal", imgFinal_resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
