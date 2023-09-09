import tensorflow as tf
import cv2
import numpy as np

class Model():

    def __init__(self, model_path):
        self.__model = tf.keras.models.load_model(model_path)
        self.color_by_index = ['none', 'yellow', 'red']
        self.__machine_status = ''
        self.__status_update_count = 0
        
    def predict(self, image):
        resized_image = cv2.resize(image, dsize=(480,480))

        # 前処理
        image_array = tf.keras.preprocessing.image.img_to_array(resized_image)
        image_array = np.expand_dims(image_array, axis=0)
        image_array /= 255.0
        
        # 各ラベルの確率を予測
        predict = self.__model.predict(image_array)  
        
        # 最も確率が高いラベルのラベル名を取得
        label_index = np.argmax(predict[0])
        color = self.color_by_index[label_index]
        score = predict[0][label_index]
        
        # 積層灯の状態を更新する
        update_flag = self.__update_status(color)
        
        return self.__machine_status, score, update_flag
    
    def __update_status(self, color):
        
        update_flag = False  # 状態アップデートの有無
        
        # 初回のみすぐに更新する
        if self.__machine_status == '': self.__machine_status = color
        
        # 状態に更新がある可能性
        if color != self.__machine_status:
            self.__status_update_count += 1
            
            # 状態の更新を行う
            if self.__status_update_count > 5:
                self.__machine_status = color
                update_flag = True
        
        return update_flag