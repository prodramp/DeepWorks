import cv2
import gradio as gr
import mediapipe as mp
import dlib
import imutils
import numpy as np


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection


def apply_media_pipe_face_detection(image):
    with mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.detections:
            return image
        annotated_image = image.copy()
        for detection in results.detections:
            mp_drawing.draw_detection(annotated_image, detection)
        return annotated_image


def apply_media_pipe_facemesh(image):
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.multi_face_landmarks:
            return image
        annotated_image = image.copy()
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
              image=annotated_image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_TESSELATION,
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles
              .get_default_face_mesh_tesselation_style())
            mp_drawing.draw_landmarks(
              image=annotated_image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_CONTOURS,
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles
              .get_default_face_mesh_contours_style())
            mp_drawing.draw_landmarks(
              image=annotated_image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_IRISES,
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles
              .get_default_face_mesh_iris_connections_style())
            return annotated_image


class FaceOrientation(object):
    def __init__(self):
        self.detect = dlib.get_frontal_face_detector()
        self.predict = dlib.shape_predictor("model/shape_predictor_68_face_landmarks.dat")

    def create_orientation(self, frame):
        draw_rect1 = True
        draw_rect2 = True
        draw_lines = True

        frame = imutils.resize(frame, width=800)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subjects = self.detect(gray, 0)

        for subject in subjects:
            landmarks = self.predict(gray, subject)
            size = frame.shape

            # 2D image points. If you change the image, you need to change vector
            image_points = np.array([
                (landmarks.part(33).x, landmarks.part(33).y),  # Nose tip
                (landmarks.part(8).x, landmarks.part(8).y),  # Chin
                (landmarks.part(36).x, landmarks.part(36).y),  # Left eye left corner
                (landmarks.part(45).x, landmarks.part(45).y),  # Right eye right corne
                (landmarks.part(48).x, landmarks.part(48).y),  # Left Mouth corner
                (landmarks.part(54).x, landmarks.part(54).y)  # Right mouth corner
            ], dtype="double")

            # 3D model points.
            model_points = np.array([
                (0.0, 0.0, 0.0),  # Nose tip
                (0.0, -330.0, -65.0),  # Chin
                (-225.0, 170.0, -135.0),  # Left eye left corner
                (225.0, 170.0, -135.0),  # Right eye right corne
                (-150.0, -150.0, -125.0),  # Left Mouth corner
                (150.0, -150.0, -125.0)  # Right mouth corner

            ])
            # Camera internals
            focal_length = size[1]
            center = (size[1] / 2, size[0] / 2)
            camera_matrix = np.array(
                [[focal_length, 0, center[0]],
                 [0, focal_length, center[1]],
                 [0, 0, 1]], dtype="double"
            )

            dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
            (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                          dist_coeffs)

            (b1, jacobian) = cv2.projectPoints(np.array([(350.0, 270.0, 0.0)]), rotation_vector, translation_vector,
                                               camera_matrix, dist_coeffs)
            (b2, jacobian) = cv2.projectPoints(np.array([(-350.0, -270.0, 0.0)]), rotation_vector,
                                               translation_vector, camera_matrix, dist_coeffs)
            (b3, jacobian) = cv2.projectPoints(np.array([(-350.0, 270, 0.0)]), rotation_vector, translation_vector,
                                               camera_matrix, dist_coeffs)
            (b4, jacobian) = cv2.projectPoints(np.array([(350.0, -270.0, 0.0)]), rotation_vector,
                                               translation_vector, camera_matrix, dist_coeffs)

            (b11, jacobian) = cv2.projectPoints(np.array([(450.0, 350.0, 400.0)]), rotation_vector,
                                                translation_vector, camera_matrix, dist_coeffs)
            (b12, jacobian) = cv2.projectPoints(np.array([(-450.0, -350.0, 400.0)]), rotation_vector,
                                                translation_vector, camera_matrix, dist_coeffs)
            (b13, jacobian) = cv2.projectPoints(np.array([(-450.0, 350, 400.0)]), rotation_vector,
                                                translation_vector, camera_matrix, dist_coeffs)
            (b14, jacobian) = cv2.projectPoints(np.array([(450.0, -350.0, 400.0)]), rotation_vector,
                                                translation_vector, camera_matrix, dist_coeffs)

            b1 = (int(b1[0][0][0]), int(b1[0][0][1]))
            b2 = (int(b2[0][0][0]), int(b2[0][0][1]))
            b3 = (int(b3[0][0][0]), int(b3[0][0][1]))
            b4 = (int(b4[0][0][0]), int(b4[0][0][1]))

            b11 = (int(b11[0][0][0]), int(b11[0][0][1]))
            b12 = (int(b12[0][0][0]), int(b12[0][0][1]))
            b13 = (int(b13[0][0][0]), int(b13[0][0][1]))
            b14 = (int(b14[0][0][0]), int(b14[0][0][1]))

            if draw_rect1 == True:
                cv2.line(frame, b1, b3, (255, 255, 0), 10)
                cv2.line(frame, b3, b2, (255, 255, 0), 10)
                cv2.line(frame, b2, b4, (255, 255, 0), 10)
                cv2.line(frame, b4, b1, (255, 255, 0), 10)

            if draw_rect2 == True:
                cv2.line(frame, b11, b13, (255, 255, 0), 10)
                cv2.line(frame, b13, b12, (255, 255, 0), 10)
                cv2.line(frame, b12, b14, (255, 255, 0), 10)
                cv2.line(frame, b14, b11, (255, 255, 0), 10)

            if draw_lines == True:
                cv2.line(frame, b11, b1, (0, 255, 0), 10)
                cv2.line(frame, b13, b3, (0, 255, 0), 10)
                cv2.line(frame, b12, b2, (0, 255, 0), 10)
                cv2.line(frame, b14, b4, (0, 255, 0), 10)

        return frame


face_orientation_obj = FaceOrientation()


class FaceProcessing(object):
    def __init__(self, ui_obj):
        self.name = "Face Image Processing"
        self.description = "Call for Face Image and video Processing"
        self.ui_obj = ui_obj

    def take_webcam_photo(self, image):
        return image

    def take_webcam_video(self, images):
        return images

    def mp_webcam_photo(self, image):
        return image

    def mp_webcam_face_mesh(self, image):
        mesh_image = apply_media_pipe_facemesh(image)
        return mesh_image

    def mp_webcam_face_detection(self, image):
        face_detection_img = apply_media_pipe_face_detection(image)
        return face_detection_img

    def dlib_apply_face_orientation(self, image):
        image = face_orientation_obj.create_orientation(image)
        return image

    def webcam_stream_update(self, video_frame):
        video_out = face_orientation_obj.create_orientation(video_frame)
        return video_out

    def create_ui(self):
        with self.ui_obj:
            gr.Markdown("Face Analysis with Webcam/Video")
            with gr.Tabs():
                with gr.TabItem("Playing with Webcam"):
                    with gr.Row():
                        webcam_image_in = gr.Image(label="Webcam Image Input", source="webcam")
                        webcam_video_in = gr.Video(label="Webcam Video Input", source="webcam")
                    with gr.Row():
                        webcam_photo_action = gr.Button("Take the Photo")
                        webcam_video_action = gr.Button("Take the Video")
                    with gr.Row():
                        webcam_photo_out = gr.Image(label="Webcam Photo Output")
                        webcam_video_out = gr.Video(label="Webcam Video")
                with gr.TabItem("Mediapipe Facemesh with Webcam"):
                    with gr.Row():
                        with gr.Column():
                            mp_image_in = gr.Image(label="Webcam Image Input", source="webcam")
                        with gr.Column():
                            mp_photo_action = gr.Button("Take the Photo")
                            mp_apply_fm_action = gr.Button("Apply Face Mesh the Photo")
                            mp_apply_landmarks_action = gr.Button("Apply Face Landmarks the Photo")
                    with gr.Row():
                        mp_photo_out = gr.Image(label="Webcam Photo Output")
                        mp_fm_photo_out = gr.Image(label="Face Mesh Photo Output")
                        mp_lm_photo_out = gr.Image(label="Face Landmarks Photo Output")
                with gr.TabItem("DLib Based Face Orientation"):
                    with gr.Row():
                        with gr.Column():
                            dlib_image_in = gr.Image(label="Webcam Image Input", source="webcam")
                        with gr.Column():
                            dlib_photo_action = gr.Button("Take the Photo")
                            dlib_apply_orientation_action = gr.Button("Apply Face Mesh the Photo")
                    with gr.Row():
                        dlib_photo_out = gr.Image(label="Webcam Photo Output")
                        dlib_orientation_photo_out = gr.Image(label="Face Mesh Photo Output")
                with gr.TabItem("Face Orientation on Live Webcam Stream"):
                    with gr.Row():
                        webcam_stream_in = gr.Image(label="Webcam Stream Input",
                                                    source="webcam",
                                                    streaming=True)
                        webcam_stream_out = gr.Image(label="Webcam Stream Output")
                        webcam_stream_in.change(
                            self.webcam_stream_update,
                            inputs=webcam_stream_in,
                            outputs=webcam_stream_out
                        )

            dlib_photo_action.click(
                self.mp_webcam_photo,
                [
                    dlib_image_in
                ],
                [
                    dlib_photo_out
                ]
            )
            dlib_apply_orientation_action.click(
                self.dlib_apply_face_orientation,
                [
                    dlib_image_in
                ],
                [
                    dlib_orientation_photo_out
                ]
            )
            mp_photo_action.click(
                self.mp_webcam_photo,
                [
                    mp_image_in
                ],
                [
                    mp_photo_out
                ]
            )
            mp_apply_fm_action.click(
                self.mp_webcam_face_mesh,
                [
                    mp_image_in
                ],
                [
                    mp_fm_photo_out
                ]
            )
            mp_apply_landmarks_action.click(
                self.mp_webcam_face_detection,
                [
                    mp_image_in
                ],
                [
                    mp_lm_photo_out
                ]
            )
            webcam_photo_action.click(
                self.take_webcam_photo,
                [
                    webcam_image_in
                ],
                [
                    webcam_photo_out
                ]
            )
            webcam_video_action.click(
                self.take_webcam_video,
                [
                    webcam_video_in
                ],
                [
                    webcam_video_out
                ]
            )

    def launch_ui(self):
        self.ui_obj.launch()


if __name__ == '__main__':
    my_app = gr.Blocks()
    face_ui = FaceProcessing(my_app)
    face_ui.create_ui()
    face_ui.launch_ui()

