import numpy as np
import cv2

min_confidence = 0.5 #Nilai minimum confidence models ketika mendeteksi wajah. Minimum 50%  objec tersebut adalah wajah
net = cv2.dnn.readNetFromCaffe("models/deploy.prototxt.txt","models/res10_300x300_ssd_iter_140000.caffemodel")
# image = cv2.imread('images/masked.jpg') #Load gambar yang nanti akan di deteksi wajahnya
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    height, width = frame.shape[0], frame.shape[1] #mengakses ukuran gambar yaitu height, width  dan disimpan dalam variabel height, width
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300,300)) , 1.0, (300,300), (104.0, 117.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    for i in range(0, detections.shape[2]):
        confidence = detections[0,0,i,2] # a
        if confidence > min_confidence:
            box = detections[0,0,i , 3:7] * np.array([width, height, width, height]) # |  
            (startX, startY, endX, endY) = box.astype('int')
            text = "{:.2f}%".format(confidence  *100)
            y = startY - 10 if startY - 10 > 10 else startY+10 # c
            cv2.rectangle(frame, (startX, startY),(endX, endY), (0,0,255), 2)                  #   |  d
            cv2.putText(frame, text, (startX, y),                #   |
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0,0,255), 2)#   |

    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1) & 0xff
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
