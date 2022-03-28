import cv2
from os import path
import serial
from numpy import array

ASSETS_PATH = path.join('MakeOhio2022', 'Make Ohio', 'python', 'assets')

class SerialMonitor():
    def init_serial_monitor(self, port, brate=9600):
        #try connecting to serial monitor
        try:
            #board = Arduino("/dev/cu.usbmodem111301")
            self.serial_monitor = serial.Serial(
                port=f'\\\\.\\{port}',
                baudrate=brate,
                parity=serial.PARITY_ODD,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            print("Connected Successfully")
        except:
            print('Disconnected')
            quit()

    def serial_write(self, val):
        if not self.serial_monitor.isOpen():
            self.serial_monitor.open()

        self.serial_monitor.write(val.encode())

class WarningModel(SerialMonitor):
    def __init__(self, scale, write_to_serial=False, serial_port='COM7'):
        #initialize camera and frames
        self._frame_scale = scale
        self.__cap = cv2.VideoCapture(0)
        self.__frame_color = []
        self.__frame_gray = []

        #get haarcascades for face and eye
        self.__face_cascade, self.__eye_cascade = self.__get_cascades()

        #update initial frame
        self.update_frame()
        
        #initialize serial monitor
        self.__write_to_serial = write_to_serial
        if self.__write_to_serial:
            self.init_serial_monitor(serial_port)        

    def __get_cascades(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        return face_cascade, eye_cascade

    def update_frame(self):
        _, frame = self.__cap.read()

        self.__frame_color = cv2.resize(frame, (0,0), fx=self._frame_scale, fy=self._frame_scale)
        self.__frame_gray = cv2.cvtColor(self.__frame_color, cv2.COLOR_BGR2GRAY)

    def get_frame_color(self):
        return self.__frame_color

    def get_frame_gray(self):
        return self.__frame_gray

    def get_faces_in_frame(self, roi, scale, min_neighbors):
        return self.__face_cascade.detectMultiScale(roi, scale, min_neighbors)
    
    def get_eyes_in_frame(self, roi, scale, min_neighbors):
        return self.__eye_cascade.detectMultiScale(roi, scale, min_neighbors)

    def exit(self):
        if self.__write_to_serial and self.serial_monitor.isOpen():
            self.serial_monitor.close()

        self.__cap.release()
        cv2.destroyAllWindows()

class DrivingModel(SerialMonitor):
    def __init__(self, frame_scale, write_to_serial=False, serial_port='COM7'):
        #intialize camera and frames
        self._frame_scale = frame_scale
        self.__cap = cv2.VideoCapture(0)
        self.__frame_color = []
        self.__frame_gray = []

        #update initial frame
        self.update_frame()

        #initialize serial monitor
        self._write_to_serial = write_to_serial
        if self._write_to_serial:
            self.init_serial_monitor(serial_port, 9600)

    def update_frame(self):
        #frame = cv2.imread(os.path.join(ASSETS_PATH, 'img.jpg'))
        _, frame = self.__cap.read()

        self.__frame_color = cv2.resize(frame, (0,0), fx=self._frame_scale, fy=self._frame_scale)
        self.__frame_gray = cv2.cvtColor(self.__frame_color, cv2.COLOR_BGR2GRAY)

    def get_frame_color(self):
        return self.__frame_color

    def get_frame_gray(self):
        return self.__frame_gray

    def get_color_mask(self):
        #get hsv
        hsv = cv2.cvtColor(self.__frame_color, cv2.COLOR_BGR2HSV)

        #hsv bounds given in BGR
        lower_blue = array([110, 50, 50])
        upper_blue = array([130, 255, 255])

        return cv2.inRange(hsv, lower_blue, upper_blue)

    def exit(self):
        if self._write_to_serial and self.serial_monitor.isOpen():
            self.serial_monitor.close()

        self.__cap.release()
        cv2.destroyAllWindows()