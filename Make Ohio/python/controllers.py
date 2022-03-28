import cv2
from numpy import flatnonzero, average
from time import time
from models import DrivingModel

# colors
BLUE = (255, 0, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)

# --WarningModel vars
# detectMultiScale parameters
F_SCALE = 1.3
E_SCALE = 1.3
F_MIN_NEIGHBORS = 5
E_MIN_NEIGHBORS = 8
# distraction times (sec)
DISTRACTED_TIME = 2
RESET_TIME = 4
UNRESPONSIVE_TIME = 4
# warning values
WARNING_1 = 3
WARNING_2 = 4
WARNING_3 = 5

# --DrivingModel vars
# movement
TOLERANCE = 0.2
STRAIGHT = 0
RIGHT = 1
LEFT = -1

class WarningController():
    '''Controller for distraction detection and warning system'''
    def __init__(self, view, model, write_to_serial=False):
        # view and model
        self.model = model
        self.view = view   

        # distraction variables
        self._distraction_level = 0
        self._visible_eyes = 0

        # timing variables
        self.__time_since_undistracted = time()
        self.__time_since_unresponive = self.__time_since_undistracted
        self.__time_since_distracted = self.__time_since_undistracted

        # event variables
        self.__reset = True
        self.__warned = True
        self.__distracted = False

        # bool if write to serial monitor
        self._write_to_serial = write_to_serial

    def update_view_to_match_model(self):
        '''Update view image to model frame'''

        self.model.update_frame()

        self.handle_events()
        self.__update_faces(self.model.get_frame_color(), self.model.get_frame_gray())

        self.view.image = self.model.get_frame_color()

    def handle_events(self):
        '''Handle all events for warning and distraction system'''

        # update times and return if currently undistracted 
        if self._visible_eyes >= 2:
            if self.__distracted:
                self.__time_since_undistracted = time()
                self.__distracted = False

            self.__time_since_distracted = time()
            self.__time_since_unresponive = self.__time_since_distracted
            self.__handle_distraction_reset_time()

            return

        # check if current distraction elevates distraction level
        self.__handle_distraction_time()
        # check if unresponsive
        self.__handle_unresponsive_time() 
        # warn if not already warned
        self.__handle_warnings()

    def __handle_warnings(self):
        # check if already warned for current distraction
        if self.__warned: return
        self.__warned = True

        # first warning
        if self._distraction_level == 1:
            self.__first_warning()

        # second warning
        elif self._distraction_level == 2:
            self.__second_warning()

        # third warning
        elif self._distraction_level >= 3:
            self.__third_warning()

    def __handle_distraction_reset_time(self):
        if self.__reset: return

        # check elapsed time since undistracted
        elapsed = time() - self.__time_since_undistracted
        if elapsed > RESET_TIME:
            self._distraction_level = 0
            self.__reset = True

            print('Distraction level reset')
            
    def __handle_unresponsive_time(self):
        if self._distraction_level < 1: return

        # check elapsed time since unresponsive
        elapsed = int(time() - self.__time_since_unresponive)
        if  elapsed == UNRESPONSIVE_TIME:
            self._distraction_level += 1
            self.__time_since_unresponive = time()
            self.__warned = False

            print('Unresponsive')

    def __handle_distraction_time(self):
        if self.__distracted: return

        # check elapsed time since distraction started
        elapsed = time() - self.__time_since_distracted
        if  elapsed > DISTRACTED_TIME:
            self._distraction_level += 1
            self.__time_since_unresponive = time()
            self.__distracted = True
            self.__warned = False
            self.__reset = False

    def __first_warning(self):
        if self._write_to_serial and self.model.serial_monitor.isOpen():
            self.model.serial_write(WARNING_1)

        print('first warning')
        
    def __second_warning(self):
        if self._write_to_serial and self.model.serial_monitor.isOpen():
            self.model.serial_write(WARNING_2)

        print('second warning')

    def __third_warning(self):
        if self._write_to_serial and self.model.serial_monitor.isOpen():
            self.model.serial_write(WARNING_3)

        print('AI taking controls')
        self.switch_to_autonomous_driving()

    def __update_faces(self, frame, roi):
        faces = self.model.get_faces_in_frame(roi, F_SCALE, F_MIN_NEIGHBORS)
        self._visible_eyes = 0

        for face in faces:
            x,y,w,h = face

            # draw face and return frame values
            cv2.rectangle(frame, (x,y,w,h), BLUE)

            eroi = frame[y:y+h, x:x+w]
            eframe = frame[y:y+h, x:x+w]

            self.__update_eyes(eframe, eroi)

    def __update_eyes(self, frame, roi,):
        # get eyes in face
        eyes = self.model.get_eyes_in_frame(roi, E_SCALE, E_MIN_NEIGHBORS)

        # number of eyes
        self._visible_eyes = len(eyes)

        # draw eyes
        for eye in eyes:
            cv2.rectangle(frame, eye, GREEN)

    def switch_to_autonomous_driving(self):
        self.model.exit()
        model = DrivingModel(0.5) 
        controller = DrivingController(self.view, model)
        self.view.set_controller(controller)

class DrivingController():
    '''Controller for self driving based on car camera using color detection'''

    def __init__(self, view, model, write_to_serial=False):
        # views and models
        self.model = model
        self.view = view

        # frame length and height
        self._height = len(self.model.get_frame_color())
        self._length = len(self.model.get_frame_color()[0])

        # distance variable
        self._distance_to_center = 0

        # bool if write to serial monitor
        self._write_to_serial = write_to_serial

    def update_view_to_match_model(self):
        '''Update view image to model frame'''

        self.model.update_frame()

        self.handle_events()
        self.__update_distance_to_center()

        self.view.image = self.model.get_frame_color()

    def handle_events(self):
        '''Handle all events '''
        # check if distance is to the positive to tolerance window
        if self._distance_to_center > self._length * TOLERANCE:
            self.__turn(RIGHT)
            
        # check if distance is negative to the tolerance window
        elif self._distance_to_center < -1 * self._length * TOLERANCE:
            self.__turn(LEFT)            

        # distance is within the tolerance window
        else:
            self.__turn(STRAIGHT)

    def __turn(self, direction):
        # unpack direction
        if (direction < 0):
            print_instruction = 'turn left'
        elif (direction > 0):
            print_instruction = 'turn right'
        else:
            print_instruction = 'go straight'

        # print instruction for debugging
        print(print_instruction)

        # write instruction to serial monitor
        if self._write_to_serial and self.model.serial_monitor.isOpen():
            self.model.serial_write(direction)

        if direction == STRAIGHT: return

        # draw red line at boundary of tolerance zone
        self.__draw_tolerance_boundary(direction)

    def __draw_tolerance_boundary(self, direction):
        # draw tolerance boundary
        x = self._length // 2 + (direction * int(self._length * TOLERANCE))
        cv2.line(self.model.get_frame_color(), \
            (x, self._height), \
                (x, self._height - 6), \
                    RED, 3)

    def __update_distance_to_center(self):
        # get average column of color
        avgCol = self.__get_avg_row_of_color()

        # draw line to x position of avg col
        cv2.line(self.model.get_frame_color(), (self._length // 2, self._height), (avgCol, self._height), GREEN, 5)

        # update distance to center of frame
        self._distance_to_center = avgCol - self._length // 2

    def __get_avg_row_of_color(self):
        # get mask of color
        mask = self.model.get_color_mask()

        # get average column of each row containing 1 (color)
        rows = [average(flatnonzero(row)) for row in mask if len(flatnonzero(row)) > 0]

        # if row has no color, return center frame
        if len(rows) < 1:
            return self._length // 2

        # return average of all rows
        return int(average(rows))