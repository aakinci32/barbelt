import face_recognition
import cv2
import numpy as np
import os
from django.conf import settings




def facialRecognition():
# Load a sample picture and learn how to recognize it.
    image_path = os.path.join(settings.BASE_DIR,'BarBelt', 'static', 'trump.jpg')

    trump_image = face_recognition.load_image_file(image_path)

    if trump_image is None:
        print("Error: 'trump.jpg' not loaded.")
    else:
        trump_face_encoding = face_recognition.face_encodings(trump_image)[0]
    # Load a second sample picture and learn how to recognize it.
    image_path2 = os.path.join(settings.BASE_DIR,'BarBelt', 'static', 'elon.jpg')

    elon_image = face_recognition.load_image_file(image_path2)
    if elon_image is None:
        print("Error: 'elon.jpg' not loaded.")
    else:
        elon_face_encoding = face_recognition.face_encodings(elon_image)[0]

    image_path3 = os.path.join(settings.BASE_DIR,'BarBelt', 'static', 'rohan.jpg')
    rohan_image = face_recognition.load_image_file(image_path3)
    if rohan_image is None:
        print("Error: 'rohan.jpg' not loaded.")
    else:
        rohan_face_encoding = face_recognition.face_encodings(rohan_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        trump_face_encoding,
        elon_face_encoding,
        rohan_face_encoding
    ]
    known_face_names = [
        "Donald Trump",
        "Elon Musk",
        "Rohan Shenoy"
    ]

    # Initialize the webcam

    video_capture = cv2.VideoCapture(1,cv2.CAP_AVFOUNDATION)
    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
    print("AFTER")
    while True:
        # Grab a single frame from the webcam
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame")
        

        # Resize the frame to speed up processing (optional)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR (OpenCV) to RGB (face_recognition)
        rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = cv2.cvtColor(rgb_small_frame , cv2.COLOR_BGR2RGB)

        
        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            # Compare the found faces with known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Find the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame was resized
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with the name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        
        # cv2.imshow('Real-Time Face Recognition', frame)

        # Hit 'q' on the keyboard to quit
        if (cv2.waitKey(1) & 0xFF == ord('q')) or name:
            print(name)
            break

    # Release the webcam and close all OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()