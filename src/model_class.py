from ultralytics import YOLO
import cv2

CONF_THD = 0.6
colors = {'red': (0, 0, 255), 'yellow': (0, 240, 255), 'none': (210, 240, 0)}

class Model():

    def __init__(self, weight_path):
        self.__model = YOLO(weight_path)
        self.__machine_status = ''
        self.__status_update_count = 0
        self.__label_prev_frame = ''

    def predict(self, image):

        results = self.__model.predict(source=image, save=False, verbose=False)
        frame_draw = image.copy()

        # 検出結果を描画する
        boxes = []
        for box in results[0].boxes:
            detected_label = results[0].names[box.cls[0].item()]

            conf = int(box.conf[0].item() * 100) # 検出の信頼度

            if conf > CONF_THD*100:
                # 検出したボックス、ラベル名、信頼度を描画する
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                frame_draw = plot_box(
                    image=frame_draw, 
                    pt1={'x': x1, 'y': y1}, 
                    pt2={'x': x2, 'y': y2},
                    label=detected_label,
                    conf=conf
                )

            # 1つのリストにまとめる
            boxes.append({'label': detected_label, 'conf': conf})
        
        # confが最大のboxを取り出す
        label = 'none'
        if len(boxes) > 0:
            max_conf_box = max(boxes, key=lambda x: x['conf'])
            if max_conf_box['conf'] > CONF_THD*100:
                label = max_conf_box['label']
            
        # 積層灯の状態を更新する
        update_flag = self.__update_status(label)
        
        return frame_draw, self.__machine_status, update_flag
    
    def __update_status(self, label):
        
        update_flag = False  # 状態アップデートの有無
        
        # 初回のみすぐに更新する
        if self.__machine_status == '': 
            self.__machine_status = label
            self.__label_prev_frame = label
        
        # 状態に更新がある可能性
        elif label != self.__machine_status:

            # カウントを重ねるためには同じ色の検知が連続する必要がある
            if self.__status_update_count < 1 or label == self.__label_prev_frame:
                self.__status_update_count += 1

            else: self.__status_update_count = 0

            self.__label_prev_frame = label
            
            # 状態の更新を行う
            if self.__status_update_count > 10:
                self.__machine_status = label
                update_flag = True
        
        else: self.__status_update_count = 0

        return update_flag
    

def plot_box(image, pt1, pt2, label, conf, padding=6, font_scale=3):

    text = f'{label} {conf}%'.upper()

    cv2.rectangle(image, (pt1['x'] - 1, pt1['y']), (pt2['x'], pt2['y']), colors[label], thickness=2, lineType=cv2.LINE_AA)
    res_scale = (image.shape[0] + image.shape[1])/1600
    font_scale = font_scale * res_scale
    font_width, font_height = 0, 0
    font_face = cv2.FONT_HERSHEY_DUPLEX
    text_size = cv2.getTextSize(text, font_face, fontScale=font_scale, thickness=1)[0]

    if text_size[0] > font_width:
        font_width = text_size[0]
    if text_size[1] > font_height:
        font_height = text_size[1]
    if pt1['x'] - 1 < 0:
        pt1['x'] = 1
    if pt1['x'] + font_width + padding*2 > image.shape[1]:
        pt1['x'] = image.shape[1] - font_width - padding*2
    if pt1['y'] - font_height - padding*2  < 0:
        pt1['y'] = font_height + padding*2
    
    p3 = pt1['x'] + font_width + padding*2, pt1['y'] - font_height - padding*2 - 20
    cv2.rectangle(image, (pt1['x'] - 2, pt1['y']-20), p3, colors[label], -1, lineType=cv2.LINE_AA)
    x = pt1['x'] + padding
    y = pt1['y'] - padding

    cv2.putText(image, text, (x, y-20), font_face, font_scale, [0, 0, 0], thickness=1, lineType=cv2.LINE_AA)
    
    return image
