import cv2
from mediapipe.python.solutions import drawing_styles, face_mesh, drawing_utils
from math import hypot

cap = cv2.VideoCapture(0)
nose_img = cv2.imread("pig_nose.png")
cap.set(3,640)
cap.set(4,480)

mpDraw = drawing_utils
mpDrawingStyles = drawing_styles
mpFaceMesh = face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=4) 

while True:
    ret,frame= cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(rgb)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # mpDraw.draw_landmarks(image=frame,
            #     landmark_list=face_landmarks,connections=mpFaceMesh.FACEMESH_TESSELATION,
            #     landmark_drawing_spec=None,
            #     connection_drawing_spec=mpDrawingStyles.get_default_face_mesh_tesselation_style()
            # )
            leftnosex = 0
            leftnosey = 0
            rightnosex = 0
            rightnosey = 0
            centernosex = 0
            centernosey = 0
            for lm_id, lm in enumerate(face_landmarks.landmark):
                h, w, c = rgb.shape                 
                x, y = int(lm.x * w), int(lm.y * h) 
                if lm_id == 49:           
                    leftnosex, leftnosey = x, y
                if lm_id == 279:          
                    rightnosex, rightnosey = x, y
                if lm_id == 5:            
                    centernosex, centernosey = x, y
            nose_width = int(hypot(rightnosex-leftnosex,rightnosey-leftnosey*1.2))    
            nose_height = int(nose_width*0.8)    
            if (nose_width and nose_height) != 0:
                pig_nose = cv2.resize(nose_img,(nose_width, nose_height))
            top_left = (int(centernosex-nose_width/2),int(centernosey-nose_height/2))
            bottom_right = (int(centernosex+nose_width/2),int(centernosey+nose_height/2))
            nose_area = frame[ top_left[1]: top_left[1]+nose_height,top_left[0]: top_left[0]+nose_width]
            pig_nose_gray = cv2.cvtColor(pig_nose, cv2.COLOR_BGR2GRAY)
            _, nose_mask = cv2.threshold(
            pig_nose_gray, 25, 255, cv2.THRESH_BINARY_INV)
            no_nose = cv2.bitwise_and(nose_area, nose_area, mask=nose_mask) #Untuk menghapus bagian hidung (menggunakan operator bitwise_and)
            final_nose = cv2.add(no_nose, pig_nose)
            frame[ top_left[1]: top_left[1]+nose_height,
            top_left[0]: top_left[0]+nose_width ] = final_nose

    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1) & 0xFF
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cap.destroyAllWindows()