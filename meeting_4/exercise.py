import cv2

img = cv2.imread('exercise.jpg')
print(img.shape)
height, width, channel = img.shape

cv2.rectangle(img,(300,20),(430,150),(0,255,0),2)
cv2.putText(img, "Face", (300, 15), 
cv2.FONT_ITALIC, 0.5 , (0,255,0), 2)

cv2.rectangle(img,(400,250),(600,400),(255,0,0),2)
cv2.putText(img, "Laptop", (400,240), 
cv2.FONT_ITALIC, 0.5 , (255,0,0), 2)

cv2.circle(img,(380,380),50,(0,0,255),2)
cv2.putText(img, "Coffe", (350,320), 
cv2.FONT_ITALIC, 0.5 , (0,0,255), 2)

cv2.imshow("Latihan",img)
cv2.waitKey(0)
cv2.destroyAllWindows()