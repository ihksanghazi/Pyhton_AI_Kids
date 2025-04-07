import cv2
import numpy as np

def getContours(img): 
     contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)                                 
     for cnt in contours:  
        area = cv2.contourArea(cnt)
        print(area)                
        cv2.drawContours(imgContour, cnt, -1, (255,0,0), 3)

img = cv2.imread("img/shape.jpg")
imgGrayScale = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGrayScale,(7,7),1)

imgCanny = cv2.Canny(imgBlur,30,30)
imgContour = img.copy()#a
getContours(imgCanny)  #b
cv2.imshow("Original Picture",img)
# cv2.imshow("GrayScale Picture",imgGrayScale)
# cv2.imshow("Blur Picture",imgBlur)
cv2.imshow("Canny Picture",imgCanny)
cv2.imshow("Contour Image", imgContour)



cv2.waitKey(0)