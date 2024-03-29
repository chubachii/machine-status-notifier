import cv2, numpy

class Camera():

    def __init__(self, camID):
        self.__camID = camID

    def open(self):
        self.__cap = cv2.VideoCapture(self.__camID)
        return self.__cap.isOpened()
    
    def read(self):
        _, frame = self.__cap.read()
        return frame
    
    def save(self, path, image):
        cv2.imwrite(path, image)  

    def wait_key(self, wait_time):
        return cv2.waitKey(wait_time)

    