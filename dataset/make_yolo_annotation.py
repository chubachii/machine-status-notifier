import os
"""
import cv2

img = cv2.imread('MSN_yolo/none/2023_09_20_17_55_18.jpg')

cv2.rectangle(img, (320, 225), (355, 270), (255, 0, 0))
cv2.rectangle(img, (int(0.526563*640), int(0.512500*480)), (int(0.526563*640+0.056250*640), int(0.512500*480+0.083333*480)), (255, 255, 0))

cv2.imshow('test', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
# red:0, yellow:1, none:2

RED = '0 0.525781 0.494792 0.054688 0.047917'
YELLOW = '1 0.527344 0.527083 0.057813 0.054167'
NONE = '2 0.528125 0.512500 0.059375 0.083333'

dir = 'MSN_yolo/images/none'
output = 'MSN_yolo/labels/none'

files = os.listdir(dir)

for file in files:
    name = os.path.splitext(os.path.basename(file))[0]
    path = os.path.join(output, name + '.txt')
    
    f = open(path, 'w')
    f.write(NONE)
    f.close()