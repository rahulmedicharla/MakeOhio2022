from cv2 import imshow

#purpose of having view is to leave room to make gui

class View():
    def __init__(self):
        self.controller = 0
        self.image = []

    def display(self):
        imshow('frame', self.image)

    def set_controller(self, controller):
        self.controller = controller