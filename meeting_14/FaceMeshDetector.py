import itertools
import numpy as np
from mediapipe.python.solutions import face_detection, drawing_utils, face_mesh, drawing_styles
import cv2

class FaceMesh:
    def __init__(self):
        self.mpFaceDetection = face_detection
        self.face_detection = self.mpFaceDetection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.5)
        self.mpDraw = drawing_utils
        self.mpFaceMesh = face_mesh
        self.faceMeshImages = self.mpFaceMesh.FaceMesh(
            static_image_mode=True, 
            max_num_faces=2,
            min_detection_confidence=0.5)
        self.faceMeshVideos = self.mpFaceMesh.FaceMesh(
            static_image_mode=False, 
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.3)
        self.mpDrawStyles = drawing_styles

    def detectFacialLandmarks(self, image, face_mesh:face_mesh.FaceMesh):
        results = face_mesh.process(image[:,:,::-1])
        output_image = image[:,:,::-1].copy() #untuk menyalin gambar dari parameter yang sudah dikirim
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(image=output_image, 
                    landmark_list=face_landmarks,
                    connections=self.mpFaceMesh.FACEMESH_TESSELATION, #Menggambar garis dari facial area yang sudah di deteksi
                    landmark_drawing_spec=None, 
                    connection_drawing_spec=self.mpDrawStyles.
                    get_default_face_mesh_tesselation_style())
                self.mpDraw.draw_landmarks(image=output_image,
                    landmark_list=face_landmarks,
                    connections=self.mpFaceMesh.FACEMESH_CONTOURS,    #Menggambar garis dari facial area yang sudah di deteksi
                    landmark_drawing_spec=None, 
                    connection_drawing_spec=self.mpDrawStyles.
                    get_default_face_mesh_contours_style())    
        return np.ascontiguousarray(output_image[:,:,::-1], dtype=np.uint8), results

    def detect_mouth_area(self, face_landmarks_result, image_height, image_width, threshold):
        # Mengembalikan indeks landmark untuk area mulut
        # Outer & inner lips kombinasi
        MOUTH_INDEXES = [[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308,
                        324, 318, 402, 317, 14, 87, 178, 88, 95]]
        return MOUTH_INDEXES

    def detect_left_eye_area(self, face_landmarks_result, image_height, image_width, threshold):
        # Mengembalikan indeks landmark untuk mata kiri (dari sudut pandang user)
        LEFT_EYE_INDEXES = [[33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157,
                            158, 159, 160, 161, 246]]
        return LEFT_EYE_INDEXES

    def detect_right_eye_area(self, face_landmarks_result, image_height, image_width, threshold):
        # Mengembalikan indeks landmark untuk mata kanan (dari sudut pandang user)
        RIGHT_EYE_INDEXES = [[263, 249, 390, 373, 374, 380, 381, 382, 362, 398, 384,
                            385, 386, 387, 388, 466]]
        return RIGHT_EYE_INDEXES


    def isOpen(self, image, face_mesh_results, face_part:str, threshold=5):
        image_height, image_width, _ = image.shape
        output_image = image.copy()
        status = {}
        if face_part == 'MOUTH':
            INDEXES = self.detect_mouth_area(face_mesh_results, image_height, image_width, threshold)
        elif face_part == 'LEFT EYE':
            INDEXES = self.detect_left_eye_area(face_mesh_results, image_height, image_width, threshold)
        elif face_part == 'RIGHT EYE':
            INDEXES = self.detect_right_eye_area(face_mesh_results, image_height, image_width, threshold)
        else:
            return
        for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
            _, height, _ = self.getSize(image, face_landmarks,INDEXES) 
            _, face_height, _ = self.getSize(
                image, face_landmarks, self.mpFaceMesh.FACEMESH_FACE_OVAL)
            if (height/face_height)*100 > threshold:
                status[face_no] = 'OPEN'  
                color = (0, 255, 0)       
            else:                         
                status[face_no] = 'CLOSE' 
                color = (0, 0, 255)       

            cv2.putText(output_image, f"FACE {face_no+1}{face_part} {status[face_no]}.",(10, image_height-40), cv2.FONT_HERSHEY_PLAIN, 1.4, color, 2)
        return output_image, status
        
    def getSize(self, image, face_landmarks, INDEXES):
        image_height, image_width, _ = image.shape
        INDEXES_LIST = list(itertools.chain(*INDEXES)) 
        landmarks = []
        for INDEX in INDEXES_LIST:                            
            landmarks.append([int(face_landmarks.landmark[INDEX].x *image_width),int(face_landmarks.landmark[INDEX].y * image_height)])#
        _, _, width, height = cv2.boundingRect(np.array(landmarks)) 
        landmarks = np.array(landmarks)
        return width, height, landmarks

    def masking(self, image, filter_img, face_landmarks, face_part, INDEXES):
        annotated_image = image.copy()
        try:
            filter_img_height, filter_img_width, _ =filter_img.shape
            _, face_part_height, landmarks = self.getSize(image, face_landmarks, INDEXES)
            required_height = int(face_part_height*2.5)
            resized_filter_img = cv2.resize(filter_img,(int(filter_img_width *(required_height/filter_img_height)),required_height))                               #|
            filter_img_height, filter_img_width, _ = resized_filter_img.shape
            _, filter_img_mask = cv2.threshold(cv2.cvtColor(resized_filter_img,cv2.COLOR_BGR2GRAY), 25, 255,cv2.THRESH_BINARY_INV)
            center = landmarks.mean(axis=0).astype("int")
            if face_part == 'MOUTH':
               location = (int(center[0] - filter_img_width / 3), int(center[1]))
            else:
                location = (int(center[0]-filter_img_width/2), int(center[1]-filter_img_height/2))
            ROI = image[location[1]: location[1] + filter_img_height,
            location[0]: location[0] + filter_img_width]
            resultant_image = cv2.bitwise_and(ROI, ROI,
                mask=filter_img_mask)
            resultant_image = cv2.add(resultant_image,
                resized_filter_img)
            annotated_image[location[1]: location[1] +
                filter_img_height, location[0]: location[0]
                + filter_img_width] = resultant_image
        except Exception as e:
            pass

        return annotated_image