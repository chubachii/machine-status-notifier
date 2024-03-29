from ultralytics import YOLO

class Model():

    def __init__(self, weight_path):
        self.__model = YOLO(weight_path)
        self.__machine_status = ''
        self.__status_update_count = 0
        self.__color_pred_frame = ''

    def predict(self, image):

        results = self.__model.predict(source=image, save=False, verbose=False)
        frame_draw = results[0].plot(font_size=30)
        
        # 検出した色を一つに絞り込む（none よりも red, yellowを優先する）
        color = 'none'
        for box in results[0].boxes:
            detected_color = results[0].names[box.cls[0].item()]
            if detected_color != 'none': color = detected_color

        # 積層灯の状態を更新する
        update_flag = self.__update_status(color)
        
        return frame_draw, self.__machine_status, update_flag
    
    def __update_status(self, color):
        
        update_flag = False  # 状態アップデートの有無
        
        # 初回のみすぐに更新する
        if self.__machine_status == '': 
            self.__machine_status = color
            self.__color_pred_frame = color
        
        # 状態に更新がある可能性
        elif color != self.__machine_status:

            # カウントを重ねるためには同じ色の検知が連続する必要がある
            if self.__status_update_count < 1 or color == self.__color_pred_frame:
                self.__status_update_count += 1

            else: self.__status_update_count = 0

            self.__color_pred_frame = color
            
            # 状態の更新を行う
            if self.__status_update_count > 10:
                self.__machine_status = color
                update_flag = True
        
        else: self.__status_update_count = 0

        return update_flag