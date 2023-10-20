from algorithm.object_detector import YOLOv7
from utils.detections import draw
import json
import cv2

class Model_yolo():

    def __init__(self, model_path, class_path):
        self.__yolov7 = YOLOv7()
        self.__yolov7.load(model_path, classes=class_path, device='cpu')
        self.predicted_color = ''
        self.__machine_status = ''

    def predict(self, image):
      
        detections = self.__yolov7.detect(image)

        # 検出したオブジェクトがあるかどうか
        if len(detections) == 0: return detections, self.__machine_status, 'none', False

        # 画像中にRED or YELLOWがあるかどうか
        color = ''
        for detection in detections:
            if detection['class'] == 'RED': color = 'red'
            elif detection['class'] == 'YELLOW': color = 'yellow'
            else: 
                if (color == '') or (color == 'none'):
                    color = 'none' 
        self.predicted_color = color

        
        # 積層灯の状態を更新する
        update_flag = self.__update_status(self.predicted_color)

        
        return detections, self.__machine_status, self.predicted_color, update_flag
    
    def __update_status(self, color):
        
        update_flag = False  # 状態アップデートの有無
        
        # 初回のみすぐに更新する
        if self.__machine_status == '': self.__machine_status = color
        
        # 状態に更新がある可能性
        elif color != self.__machine_status:
            self.__status_update_count += 1
            
            # 状態の更新を行う
            if self.__status_update_count > 3:
                self.__machine_status = color
                update_flag = True
        
        else: self.__status_update_count = 0

        return update_flag

    def draw_predict(self, frame, detections):
        detected_frame = draw(frame, detections)
        detected_frame = cv2.resize(detected_frame, (800, 600))
        cv2.imshow('predict', detected_frame)
        cv2.moveWindow('predict', 470, 0)