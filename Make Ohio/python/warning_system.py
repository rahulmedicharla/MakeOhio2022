import cv2
import driving
from delete_files import deleteAllButMostRecentFiles
from pyfirmata import Arduino
import serial

PORT = 'COM7'

#link to serial/arduino
# try:
#     #board = Arduino("/dev/cu.usbmodem111301")
#     ser = serial.Serial(
#         port=f'\\\\.\\{PORT}',
#         baudrate=9600,
#         parity=serial.PARITY_ODD,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS
#     )
#     print("Connected Successfully")
# except:
#     print('Disconnected')
#     quit()

#opencv data sets
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

#warning values
WARNING_1 = 3
WARNING_2 = 4
WARNING_3 = 5

#colors
BLUE = (255, 0, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)

#detectMultiScale parameters
F_SCALE = 1.3
E_SCALE = 1.3
F_MIN_NEIGHBORS = 5
E_MIN_NEIGHBORS = 8

#distraction levels
DISTRACTED_SECONDS = 3
DISTRACTED_THRESHOLD = 5 * DISTRACTED_SECONDS
RESET_TIME = 30
TAKE_OVER_TIME = 30

#on/off state
OFF = 0
ON = 1

#detect faces in frame
def detectFaces(roi, scale, minNeighbors):
    return face_cascade.detectMultiScale(roi, scale, minNeighbors)

#detect eyes in frame
def detectEyes(roi, scale, minNeighbors):
    return eye_cascade.detectMultiScale(roi, scale, minNeighbors)

#draw rectangle for face
def drawFace(frame, face, color):
    x, y, w, h = face
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    return x, y, w, h

#draw rectangle for eye
def drawEye(frame, eye, color):
    x, y, w, h = eye
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

def drawFacesAndEyes(frame, gray, faces, color):
    num_eyes = 0
    for face in faces:
            #draw face and return frame values
            x,y,w,h  = drawFace(frame, face, BLUE)

            #eyes frame and eyes grayscale
            eroi = gray[y:y+h, x:x+w]
            eframe = frame[y:y+h, x:x+w]

            #get eyes
            eyes = detectEyes(eroi, E_SCALE, E_MIN_NEIGHBORS)

            #number of eyes
            num_eyes = len(eyes)

            #draw eyes
            for eye in eyes:
                drawEye(eframe, eye, GREEN)
    
    return num_eyes

def updateTimeAndDistractions(time, repeated_distractions):
    if time > RESET_TIME:
        return 0, 0
    else:
        return time, repeated_distractions

def handleWarnings(repeated_distractions, time_unresponsive):
    if repeated_distractions > 2 or time_unresponsive > TAKE_OVER_TIME:
        lastWarning()
    elif repeated_distractions == 2 or time_unresponsive > TAKE_OVER_TIME // 2:
        secondWarning()
    elif repeated_distractions == 1:
        firstWarning()
    

def firstWarning():
    print('first warning')

    # if not ser.isOpen():
    #     ser.open()
    # ser.write(WARNING_1.encode())

def secondWarning():
    print('second warning')

    # if not ser.isOpen():
    #     ser.open()
    # ser.write(WARNING_2.encode())

def lastWarning():
    print('AI taking controls')
    driving.run()
    

    # if not ser.isOpen():
    #     ser.open()
    # ser.write(WARNING_3.encode())

#open camera
cap = cv2.VideoCapture(0)

def run():
    #initialize duration of eyes closed
    duration_eyes_closed = 0
    repeated_distractions = 0
    time_until_reset = 0
    time_unresponsive = 0
    distracted_event = False
    warned_event = True
    unresponsive_event = False
    #ser.open()

    deleteAllButMostRecentFiles()
    while True:
        #get frame
        _, frame = cap.read()
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        #get grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #get faces
        faces = detectFaces(gray, F_SCALE, F_MIN_NEIGHBORS)

        #draw faces and get eyes in frame
        num_eyes = drawFacesAndEyes(frame, gray, faces, BLUE)
        
        #check eyes are detected
        if num_eyes < 2:
            duration_eyes_closed += 1
        else:
            duration_eyes_closed = 0
            distracted_event = False
            unresponsive_event = False
            time_unresponsive = 0

        #check distraction duration
        if not distracted_event and duration_eyes_closed > DISTRACTED_THRESHOLD:
            repeated_distractions += 1
            distracted_event = True
            warned_event = False
            time_until_reset = 0
        
        if repeated_distractions > 0 and num_eyes >= 2:
            time_until_reset += 1
        elif repeated_distractions > 0 and num_eyes < 2:
            time_unresponsive += 1

        time_until_reset, repeated_distractions = updateTimeAndDistractions(time_until_reset, repeated_distractions)

        if warned_event and not unresponsive_event and time_unresponsive == TAKE_OVER_TIME // 2 + 1:
            handleWarnings(repeated_distractions, time_unresponsive)
        elif warned_event and not unresponsive_event and time_unresponsive == TAKE_OVER_TIME + 1:
            handleWarnings(repeated_distractions, time_unresponsive)
            unresponsive_event = True

        if not warned_event:
            handleWarnings(repeated_distractions, time_unresponsive)    
            warned_event = True
        
        #show frame
        cv2.imshow('frame', frame)

        #close window
        if cv2.waitKey(100) == ord('q'):
            break

    #kill camera feed
    #ser.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run()