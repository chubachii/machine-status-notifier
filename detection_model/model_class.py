import tensorflow as tf
import cv2
import numpy as np

class Model():

    def __init__(self, model_path):
        self.__model = tf.keras.models.load_model(model_path)
        self.__model_conv = tf.keras.models.Model(inputs=self.__model.input, outputs=self.__model.get_layer('block5_pool').output)
        self.color_by_index = ['none', 'yellow', 'red']
        self.__predicted_label_index = 0
        self.predicted_color = ''
        self.__machine_status = ''
        self.__status_update_count = 0

    def draw_heatmap(self, image):
        
        # 前処理
        resized_image = cv2.resize(image, dsize=(480,480))
        image_array = tf.keras.preprocessing.image.img_to_array(resized_image)
        image_array = np.expand_dims(image_array, axis=0)
        image_array /= 255.0
        
        # 各ラベルの確率を予測
        activation = self.__model_conv.predict(image_array)  

        #空のヒートマップ 
        heatmap = np.zeros(dtype = np.float32, shape = (len(activation[0][:, 0, 0]), len(activation[0][0, :, 0])))
        
        # 各フィルターについて計算
        for j in range(512):
            
            # ラベルに対応する重みを取得
            weight = self.__model.get_layer("dense").get_weights()[0][j][self.__predicted_label_index]

            # 重みが正の時
            if weight > 0:
                heatmap += activation[0][:, :, j] * weight
            else:
                heatmap -= activation[0][:, :, j] * weight

        # ヒートマップを整える
        heatmap = self.__normarize_image(heatmap)  # 正規化
        heatmap_resized = cv2.resize(heatmap, (640, 480))  # サイズを 元画像のサイズに
        heatmap_colored = cv2.applyColorMap(heatmap_resized, cv2.COLORMAP_JET) # カラーマップを適用    
        
        # 入力画像の用意
        ALPHA=0.5
        heatmap_overlay = cv2.addWeighted(image, ALPHA, heatmap_colored, 1 - ALPHA, 0)
        return heatmap_overlay

    def predict(self, image):
      
        # 前処理
        resized_image = cv2.resize(image, dsize=(480,480))
        image_array = tf.keras.preprocessing.image.img_to_array(resized_image)
        image_array = np.expand_dims(image_array, axis=0)
        image_array /= 255.0
        
        # 各ラベルの確率を予測
        predict = self.__model.predict(image_array)  
        
        # 最も確率が高いラベルのラベル名を取得
        self.__predicted_label_index = np.argmax(predict[0])
        self.predicted_color = self.color_by_index[self.__predicted_label_index]
        score = predict[0][self.__predicted_label_index]
        
        # 積層灯の状態を更新する
        if score > 0.7:
            update_flag = self.__update_status(self.predicted_color)
        else:
            update_flag = False
        
        return self.__machine_status, self.predicted_color, score, update_flag
    
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

    def __normarize_image(self, image: np.ndarray):
        image = image - np.min(image)             # 最小値が 0 になるように移動
        image = image / np.max(image)             # 0-1 の間に正規化
        image = (image * 255).astype("uint8")   # 0-255 に  float から int に
        return image