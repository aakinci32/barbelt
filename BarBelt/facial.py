import face_recognition
import cv2
import numpy as np
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse






def facialRecognition(request):
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

    # image_path3 = os.path.join(settings.BASE_DIR,'BarBelt', 'static', 'rohan.jpg')
    # rohan_image = face_recognition.load_image_file(image_path3)
    # if rohan_image is None:
    #     print("Error: 'rohan.jpg' not loaded.")
    # else:
    #     rohan_face_encoding = face_recognition.face_encodings(rohan_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        trump_face_encoding,
        elon_face_encoding,
        # rohan_face_encoding
    ]
    known_face_names = [
        "Donald Trump",
        "Elon Musk"
        # "Rohan Shenoy"
    ]

    # Initialize the webcam

    video_capture = cv2.VideoCapture(1,cv2.CAP_AVFOUNDATION)
    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return
    while True:
        # Grab a single frame from the webcam
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame")
            break
        

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
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                request.session['name'] = name
                return redirect('login_successful')

            else:
                print("no match")
                return redirect ('takePhoto')


            
            face_names.append(name)

        if len(face_names) == 0:
            continue

       
        if (cv2.waitKey(1) & 0xFF == ord('q')) or name:
            break

    # Release the webcam and close all OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()


