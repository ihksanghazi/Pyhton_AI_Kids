import itertools
import numpy as np
from mediapipe.python.solutions import face_detection, drawing_utils, face_mesh, drawing_styles

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