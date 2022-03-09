import cv2, os, serial, numpy as np
from delete_files import deleteAllButMostRecentFiles
from pyfirmata import Arduino

PORT = 'COM7'
    
#link to serial/arduino
try:
    #board = Arduino("/dev/cu.usbmodem111301")

    ser = serial.Serial(
        port= f'\\\\.\\{PORT}',
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
    print("Connected Successfully")
except:
    print('Disconnected')
    quit()

ASSETS_PATH = os.path.join('MakeOhio2022', 'Make Ohio', 'python', 'assets')

TOLERANCE = 0.3
STRAIGHT = 0
TURN_RIGHT = 1
TURN_LEFT = 2

#calc average column of color
def calcColRowAvg(array):
    avgSum = 0
    totalRows = len(array)
    rowCount = 0

    for i, row in enumerate(array):
        containsColor = False
        colSum = 0
        count = 0
        for j, el in enumerate(row):
            if el == 255:
                colSum += j
                count += 1
                if not containsColor:
                    containsColor = True

        if containsColor:
            rowCount += 1
            rowAvg = colSum / count
            if rowAvg <= totalRows * 2:
                avgSum += rowAvg

    
    if rowCount > 0:
        return int(avgSum / rowCount)
    else:
        return 0

#calc distance of average col to center of frame
def calcDistanceToCenter(frame, avgCol):
    cv2.line(frame, (len(frame[0]) // 2, len(frame) - 2), (avgCol, len(frame) - 2), (0, 255, 0), 3)

    return avgCol - len(frame[0]) // 2

#movement commands for moving to center    
def moveToCenter(distance_to_center, totalCols):
    if distance_to_center > totalCols + (totalCols * TOLERANCE):
        print('turn right')

        if not ser.isOpen():
            ser.open()
        ser.write(TURN_RIGHT.encode())
    elif distance_to_center < totalCols - (totalCols * TOLERANCE):
        print('turn left')

        if not ser.isOpen():
            ser.open()
        ser.write(TURN_LEFT.encode())
    else:
        print('centered')

        if not ser.isOpen():
            ser.open()
        ser.write(STRAIGHT.encode())

def run():
    ser.open()
    running = True

    while running:
        deleteAllButMostRecentFiles()
        img = cv2.imread(os.join(ASSETS_PATH, 'img.jpg'))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_red = np.array([110, 50, 50])
        upper_red = np.array([130, 255, 255])

        mask = cv2.inRange(hsv, lower_red, upper_red)

        avgCol = calcColRowAvg(mask)

        result = cv2.bitwise_and(img, img, mask=mask)

        distance_to_center = calcDistanceToCenter(result, avgCol)

        moveToCenter(distance_to_center, len(img[0]))

        cv2.imshow('img', img)

        if cv2.waitKey(100) == ord('q'):
            running = False
            break
    
    if ser.open():
        ser.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run()