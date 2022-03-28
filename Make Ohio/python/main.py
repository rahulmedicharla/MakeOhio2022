from delete_files import deleteAllButMostRecentFiles
import view, models, controllers
import cv2
import os

CAR_CAM_IMG_PATH = os.path.join('Make Ohio', 'python', 'assets')

def main():
    model = models.WarningModel(0.5)
    v = view.View()
    controller = controllers.WarningController(v, model)
    v.set_controller(controller)
    
    while True:
        deleteAllButMostRecentFiles(CAR_CAM_IMG_PATH)

        v.controller.update_view_to_match_model()

        v.display()

        if cv2.waitKey(100) == ord('q'):
            break
    model.exit()

if __name__ == '__main__':
    main()