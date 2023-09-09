from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf
import cv2
import datetime
import os
import json

# settings ファイル読み込み
with open(os.path.join(os.path.dirname(__file__), 'settings.json')) as f: 
    config: dict = json.load(f)
    
TOKEN = config['token']

dt_now = datetime.datetime.now()
today = dt_now.strftime('%Y_%m_%d')
save_dir = config['save_dir'] + today
os.makedirs(save_dir, exist_ok = True)

cap = cv2.VideoCapture(0)

count = 0

color_value = {'none': (255, 0, 0), 'yellow': (0, 165, 255), 'red': (0, 0, 255)}
color_index = ['none', 'yellow', 'red']

model = tf.keras.models.load_model(config['model_path'])
#model = keras.applications.vgg16.VGG16(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000)

while(cap.isOpened()):

    _, frame = cap.read()

    img = cv2.resize(frame, dsize=(480,480))

    # 前処理
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255.0

    
    pred = model.predict(x)  

    draw = frame.copy()

    index = np.argmax(pred[0]) 

    cv2.putText(draw, 
        text=color_index[index] + ' : ' + str(round(pred[0][index]*100, 3)) + '%', 
        org=(80, 450), 
        fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
        fontScale=1.8, 
        color=color_value[color_index[index]], 
        thickness=2
    )

    cv2.imshow("Camera", draw)
    
    if count > 19:
        dt_now = datetime.datetime.now()
        now = dt_now.strftime('%Y_%m_%d_%H_%M_%S')
        cv2.imwrite(os.path.join(save_dir, now + '.jpg'), frame)
        count = 0
    count += 1    
    
    if cv2.waitKey(2000) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()


