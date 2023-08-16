from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf
import cv2

cap = cv2.VideoCapture(1)


while(cap.isOpened()):

    _, frame = cap.read()
    
    #frame = cv2.imread('test/3.jpg')

    img = cv2.resize(frame, dsize=(480,480))

    # 前処理
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255.0

    model = tf.keras.models.load_model('machine-status-softmax.h5')
    #model = keras.applications.vgg16.VGG16(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000)
    pred = model.predict(x)  
    
    print('点灯無し' + str(pred[0][0]*100) + '% ' + '黄' + str(pred[0][1]*100) + '% '+ '赤' + str(pred[0][2]*100) + '% ')

    #if pred[0][0] > 0.5:
        #cv2.putText(frame, text='orange: ' + str(round(pred[0][0]*100, 3)) + '%', org=(150, 450), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(0, 165, 255), thickness=2)
    #else:
        #cv2.putText(frame, text='red: ' + str(round(100-pred[0][0]*100, 3)) + '%', org=(150, 450), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(0, 0, 255), thickness=2)


    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()


