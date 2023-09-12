import cv2

class Camera():

    def __init__(self, camID):
        self.__camID = camID
        self.color_value = {'none': (255, 0, 0), 'yellow': (0, 165, 255), 'red': (0, 0, 255)}

    def open(self):
        self.__cap = cv2.VideoCapture(self.__camID)
        return self.__cap.isOpened()
    
    def read(self):
        _, frame = self.__cap.read()
        return frame
    
    def save(self, path, image):
        cv2.imwrite(path, image)
    
    def show_frame(self, frame):
        cv2.imshow('frame', frame)        

    def wait_key(self, wait_time):
        return cv2.waitKey(wait_time)
    
    def show_status(self, image, status, score):
        
        cv2.putText(image, 
            text=status + ' : ' + str(round(score*100, 3)) + '%', 
            org=(80, 450), 
            fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale=1.8, 
            color=self.color_value[status], 
            thickness=2
        )
        
        cv2.imshow('status', image)
    